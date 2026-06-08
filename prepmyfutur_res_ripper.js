(() => {
    let results = [];
    // Target all row elements, which wrap the questions and answers
    const rows = document.querySelectorAll('.row');

    rows.forEach(row => {
        const questionCol = row.querySelector('.question');
        if (!questionCol) return; // Skip rows that aren't questions

        // 1. Extract the Question/Context
        const instructionNode = questionCol.querySelector('[id^="instructions_preview"]');
        const questionText = instructionNode ? instructionNode.innerText.trim() : 'No text found';

        // 2. Extract Choices and Status
        const answerNodes = questionCol.querySelectorAll('.answer');
        let choices = [];
        let userChoice = null;
        let correctChoice = null;

        answerNodes.forEach(node => {
            // Skip hidden answer slots (e.g., empty E, F, G, H slots)
            if (node.style.display === 'none') return;

            const textNode = node.querySelector('.answer-text');
            if (!textNode) return;
            
            let text = textNode.innerText.trim();
            
            // Find the letter choice (A, B, C, D)
            let letterNode = node.querySelector('.rep-checkbox:not(.check_or_unchecked)') || node.querySelector('.rep-checkbox');
            let letter = letterNode ? letterNode.innerText.trim() : '-';

            let fullText = `${letter}) ${text}`;
            choices.push(fullText);

            // Determine if this is the correct answer
            if (node.classList.contains('right')) {
                correctChoice = fullText;
            }
            
            // Determine if this is the answer the user clicked
            if (node.classList.contains('checked') || node.classList.contains('wrong') || node.querySelector('.check_or_unchecked.checked')) {
                userChoice = fullText;
            }
        });

        // 3. Extract the Explanation
        const explNode = row.querySelector('[id^="solution_explanation_preview"]');
        const explanation = explNode ? explNode.innerText.trim() : 'No explanation provided.';

        // Format the output cleanly
        results.push(
            `### Question ${results.length + 1}\n` +
            `**Context/Question:**\n${questionText}\n\n` +
            `**Options:**\n${choices.join('\n')}\n\n` +
            `**Your Answer:** ${userChoice || 'Unknown/Blank'}\n` +
            `**Correct Answer:** ${correctChoice || 'Unknown'}\n\n` +
            `**Explanation:**\n${explanation}\n` +
            `---`
        );
    });

    const finalString = results.join('\n\n');
    
    // Automatically copy the formatted string to the user's clipboard
    copy(finalString);
    
    console.log("%c✅ Extraction Complete!", "color: #4CAF50; font-size: 16px; font-weight: bold;");
    console.log("The data has been neatly formatted and copied to your clipboard. You can now paste it directly into the chat.");
    
    return "Ready to paste!";
})();