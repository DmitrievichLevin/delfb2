# 🇫🇷 DELF B2 Cinematic Mock Exam & Analytics Engine

A brutally difficult, terminal-based DELF B2 / DALF C1 mock exam built with Python.

Instead of asking you about generic weather patterns or ordering croissants, this 100-question exam is derived entirely from the dialogue, sarcasm, and implicit cultural contexts of popular French cinema and television.

## 📖 The Backstory

This project was born out of sheer panic and spite. After surviving a 250-day Duolingo streak, I took the TEF Études in May. Because I am an academic weapon, I purchased a *PrepMyFuture* module exactly one day before the test... only to find out the access code wouldn't arrive for days. I walked in blind and scraped a B1.

A B1 won't cut it for my academic goals. With the DELF B2 looming, I needed to aggressively target the specific grammatical and cultural traps that native English speakers fall into. So, I built my own exam. I ran the simulation on myself, scored a 76% (solid B2+!), but learned through the script's analytics that I spent an agonizing 9 hours over-analyzing C1-level distractors.

Learn from my mistakes. Use this tool. Watch your time.

## 🎬 The Source Material

The question bank (`QBankB2.json`) contains 100 unique, hand-crafted questions based on the contexts and subtitles of:

* *Dix Pour Cent* (Call My Agent!)
* *Plan Cœur* (The Hook Up Plan)
* *Comme t'y es belle !*
* *Tapie*
* *Le Dîner de Cons* (The Dinner Game)

## 🧠 What it Tests

This isn't your standard textbook quiz. It aggressively targets the nuances between a B1 and a B2/C1 speaker:

* **The "Subjonctif Irrégulier":** Beyond *il faut que je fasse*—testing *savoir*, *pouvoir*, and *aller* under pressure.
* **Chronology & Tense Mapping:** Forcing the correct usage of the *plus-que-parfait* and punishing direct translations of the English Present Perfect Continuous (knowing when to use *depuis*, *pendant*, *pour*, *en*, and *dans*).
* **Movement Verbs:** The surgical distinction between *amener/apporter*, *rentrer/retourner/revenir*, and *partir/sortir/quitter*.
* **Sarcasm, Irony, & The "Antiphrase":** Identifying when a character is using highly polite or positive words (*sourire narquois*, *prouesse*) to completely destroy someone.
* **Administrative & Professional Jargon:** *Résiliation, échéance, préavis, virement*—the vocabulary required to survive French bureaucracy.

## 🚀 Features

* **Terminal UI:** Renders questions in clean, responsive Unicode boxes.
* **Time Tracking:** Silently tracks exactly how many seconds you spend on each specific question and category.
* **Instant Feedback:** Provides immediate, detailed explanations and rule breakdowns upon answering incorrectly.
* **Analytics Generation:** Automatically generates an `erreurs_analyse.txt` report upon completion, detailing your overall score, your speed per category, and a comprehensive ledger of every mistake you made so you can spot your patterns.

## 🛠️ Installation & Usage

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/DmitrievichLevin/delfb2.git](https://github.com/DmitrievichLevin/delfb2.git)
   cd delfb2
    ```

1. **Ensure prerequisites:**
You just need Python 3.x installed on your machine. No external libraries or `pip install` required!
1. **Run the exam:**

    ```bash
    python b2_exam.py

    ```

1. **Review your analytics:**
Once you finish (or if you gracefully exit using `Ctrl+C`), open the newly generated `erreurs_analyse.txt` in your root folder to review your performance metrics.

## 📂 File Structure

* `b2_exam.py`: The main Python script that drives the terminal UI, logic, and analytics.
* `QBankB2.json`: The 100-question bank formatted in JSON.
* `erreurs_analyse.txt`: A sample output file demonstrating the post-exam analytics report.

## 💡 Advice for Test Takers

If you take this mock exam, **watch your time**. The distractors are built to make you overthink. If you are spending more than 2 minutes on a question, your brain is likely falling for a scope distractor. Go with your gut, learn the collocations, and *merde* for your exam!
