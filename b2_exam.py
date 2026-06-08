import os
import random
import sys
import textwrap
import json
import time

# ANSI escape codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# 1. Get the absolute directory of the currently running script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def render_document(text, width=65):
    """Draws a responsive Unicode box around the provided text to simulate physical documents."""
    lines = text.strip().split("\n")
    wrapped_lines = []

    # Handle wrapping while preserving explicit line breaks
    for line in lines:
        if line.strip() == "":
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(textwrap.wrap(line, width - 4))

    # Draw the top border
    print(f"  {BOLD}╭{'─' * (width - 2)}╮{RESET}")

    # Draw the content with side borders
    for line in wrapped_lines:
        print(f"  {BOLD}│{RESET} {line:<{width - 4}} {BOLD}│{RESET}")

    # Draw the bottom border
    print(f"  {BOLD}╰{'─' * (width - 2)}╯{RESET}\n")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_exam(questions):
    random.shuffle(questions)
    score = 0
    total_in_bank = len(questions)
    questions_attempted = 0

    # Trackers for analytics
    category_scores = {}
    category_totals = {}
    category_times = {}  # Tracks total time spent per category
    incorrect_questions = []

    # Start the timer
    start_time = time.time()

    try:
        for i, q in enumerate(questions):
            clear_screen()

            # Calculate elapsed time for the "Live" test timer header
            current_elapsed = time.time() - start_time
            el_m, el_s = divmod(int(current_elapsed), 60)

            print(
                f"{BOLD}{CYAN}=========================================={RESET}"
            )
            print(
                f"{BOLD}{CYAN}      🎯 DELF B2 TARGETED EXAM SIM        {RESET}"
            )
            print(
                f"{BOLD}{CYAN}=========================================={RESET}"
            )
            print(
                f"{BOLD}{YELLOW}⏱️  Temps écoulé global : {el_m:02d}:{el_s:02d}{RESET}\n"
            )

            raw_category = q.get("category", "Non classé")
            # Extract base category
            base_category = str(raw_category).split("-")[0].strip()

            print(
                f"{BOLD}Question {i + 1} of {total_in_bank} - [{raw_category}]{RESET}\n"
            )

            # Start timing the specific question (includes reading time)
            q_start_time = time.time()

            # Render the document box if it exists
            if "document" in q:
                render_document(q["document"])

            # Render ASCII art if it exists
            if "ascii_art" in q:
                print(f"{CYAN}{q['ascii_art']}{RESET}\n")

            print(f"{q['question']}\n")

            for key, value in q["options"].items():
                print(f"  {BOLD}{key}){RESET} {value}")

            answer = ""
            while answer not in ["A", "B", "C", "D"]:
                answer = (
                    input("\nVotre réponse (A/B/C/D): ")
                    .strip()
                    .upper()
                )

            # Stop timing the specific question
            q_end_time = time.time()
            time_spent_on_q = q_end_time - q_start_time

            # Tally metrics
            if base_category not in category_totals:
                category_totals[base_category] = 0
                category_scores[base_category] = 0
                category_times[base_category] = 0.0

            category_totals[base_category] += 1
            category_times[base_category] += time_spent_on_q
            questions_attempted += 1

            print("\n" + "-" * 40)
            print(
                f"⏱️  {BOLD}Temps pris pour cette question :{RESET} {time_spent_on_q:.1f} secondes"
            )

            if answer == q["answer"]:
                print(f"{GREEN}{BOLD}✅ Correct !{RESET}")
                score += 1
                category_scores[base_category] += 1
            else:
                print(
                    f"{RED}{BOLD}❌ Incorrect.{RESET} La bonne réponse était {q['answer']}."
                )

                # Log the incorrect question with its specific time metric
                incorrect_questions.append(
                    {
                        "category": raw_category,
                        "question": q["question"],
                        "options": q["options"],
                        "user_answer": answer,
                        "correct_answer": q["answer"],
                        "explanation": q["explanation"],
                        "time_spent": time_spent_on_q,
                    }
                )

            print(f"{YELLOW}Explication:{RESET} {q['explanation']}")
            print("-" * 40 + "\n")

            input(
                f"Appuyez sur {BOLD}Entrée{RESET} pour continuer..."
            )

    except KeyboardInterrupt:
        # Catch a manual exit and immediately proceed to scoring
        print(
            f"\n\n{YELLOW}{BOLD}⚠️  Test interrompu par l'utilisateur !{RESET} Calcul des résultats partiels en cours...\n"
        )
        time.sleep(1)
        clear_screen()

    # End global timer
    end_time = time.time()
    time_taken = end_time - start_time
    minutes = int(time_taken // 60)
    seconds = int(time_taken % 60)

    # Handle edge case where user exits on the very first question
    if questions_attempted == 0:
        print(
            f"{YELLOW}Aucune question complétée. Fin de la session.{RESET}\n"
        )
        return

    # Final Score Output
    clear_screen()
    print(
        f"{BOLD}{CYAN}=========================================={RESET}"
    )
    print(f"{BOLD}🎯 RÉSULTATS DU TEST & ANALYSE DE TEMPS{RESET}")
    print(
        f"{BOLD}{CYAN}=========================================={RESET}\n"
    )

    percentage = (
        (score / questions_attempted) * 100
        if questions_attempted > 0
        else 0
    )

    print(
        f"{BOLD}Score Global : {score}/{questions_attempted} ({percentage:.0f}%) - {questions_attempted} questions tentées sur {total_in_bank}{RESET}"
    )
    print(
        f"{BOLD}Temps total écoulé : {minutes} minutes et {seconds} secondes{RESET}\n"
    )

    # Detailed Category & Time Breakdown
    print(f"{BOLD}Détail par catégorie (Score & Vitesse) :{RESET}")
    print("-" * 65)
    for cat in sorted(category_totals.keys()):
        cat_total = category_totals[cat]
        cat_score = category_scores[cat]
        cat_time = category_times[cat]

        cat_pct = (
            (cat_score / cat_total) * 100 if cat_total > 0 else 0
        )
        avg_time_per_q = (
            (cat_time / cat_total) if cat_total > 0 else 0
        )

        # Colorize the percentage based on performance
        if cat_pct >= 80:
            color = GREEN
        elif cat_pct >= 50:
            color = YELLOW
        else:
            color = RED

        print(
            f"  • {cat:<20} : {cat_score}/{cat_total} ({color}{cat_pct:>3.0f}%{RESET}) | Moyenne: {BOLD}{avg_time_per_q:>4.1f}s{RESET} / question"
        )
    print("-" * 65 + "\n")

    if percentage >= 80:
        print(
            f"{GREEN}Excellent ! Vous maîtrisez les pièges du niveau B2.{RESET}"
        )
    elif percentage >= 50:
        print(
            f"{YELLOW}Pas mal, mais il reste des nuances à consolider.{RESET}"
        )
    else:
        print(
            f"{RED}Continuez à réviser vos collocations et votre vocabulaire professionnel.{RESET}"
        )

    # Write incorrect questions and time analytics to a readable log file
    if incorrect_questions:
        log_filename = "erreurs_analyse.txt"
        try:
            # 2. Join the script directory with your log filename
            LOG_PATH = os.path.join(SCRIPT_DIR, log_filename)
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                f.write(
                    "========================================================\n"
                )
                f.write(
                    "      ANALYSE DES ERREURS ET DU TEMPS - DELF B2         \n"
                )
                f.write(
                    "========================================================\n\n"
                )
                f.write(
                    f"Score final        : {score}/{questions_attempted} ({percentage:.0f}%)\n"
                )
                f.write(
                    f"Temps total écoulé : {minutes} min {seconds} sec\n\n"
                )

                f.write("--- VITESSE PAR CATÉGORIE ---\n")
                for cat in sorted(category_totals.keys()):
                    avg_t = category_times[cat] / category_totals[cat]
                    f.write(
                        f"  • {cat:<20} : {avg_t:.1f} sec / question en moyenne\n"
                    )
                f.write("\n")

                f.write("--- DÉTAIL DES ERREURS ---\n\n")
                for idx, err in enumerate(incorrect_questions, 1):
                    f.write(
                        f"Erreur #{idx} - Catégorie : {err['category']}\n"
                    )
                    f.write(
                        f"Temps de réponse : {err['time_spent']:.1f} secondes\n"
                    )
                    f.write(f"Question : {err['question']}\n\n")
                    f.write("Options :\n")
                    for k, v in err["options"].items():
                        f.write(f"  {k}) {v}\n")

                    f.write(
                        f"\nVotre réponse   : {err['user_answer']} (Incorrecte)\n"
                    )
                    f.write(
                        f"Bonne réponse   : {err['correct_answer']}\n"
                    )
                    f.write(
                        f"Explication     : {err['explanation']}\n"
                    )
                    f.write("-" * 56 + "\n\n")

            print(
                f"\n{BOLD}{CYAN}📝 Un rapport détaillé incluant vos métriques de temps a été généré : {log_filename}{RESET}"
            )
            print(
                f"{CYAN}Ouvrez ce fichier pour analyser où vous perdez du temps ou faites des erreurs.{RESET}\n"
            )

        except Exception as e:
            print(
                f"\n{RED}Erreur lors de la création du fichier d'analyse : {e}{RESET}\n"
            )
    else:
        print(
            f"\n{GREEN}{BOLD}Aucune erreur ! Aucun rapport généré.{RESET}\n"
        )


if __name__ == "__main__":
    try:

        # 2. Join that directory path with your JSON file name
        JSON_PATH = os.path.join(SCRIPT_DIR, "QBankB2.json")

        # 3. Open the file using the absolute path
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            QUESTION_BANK = json.load(file)

        run_exam(QUESTION_BANK)

    except FileNotFoundError:
        print(
            f"\n{RED}{BOLD}Erreur :{RESET} Le fichier 'QBankB2.json' est introuvable."
        )
        print(
            "Veuillez vous assurer qu'il se trouve dans le même dossier que ce script."
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"\n{RED}{BOLD}Erreur :{RESET} Le fichier 'QBankB2.json' n'est pas un JSON valide."
        )
        print("Veuillez vérifier la syntaxe de votre fichier.")
        sys.exit(1)
    except KeyboardInterrupt:
        # This will now only trigger if the user interrupts BEFORE the exam begins
        print(
            f"\n{RED}Lancement annulé.{RESET} Bon courage pour vos révisions !"
        )
        sys.exit(0)
