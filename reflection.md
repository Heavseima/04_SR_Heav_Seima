# Reflection

Building this app helped me understand how the parts of a RAG system work together. Keeping each part in its own file made the code easier to read and fix. Saving the index also worked well because I could close the app and use it again without repeating the setup. I liked seeing the retrieved text before the answer. It helped me check where the answer came from and whether it matched the text.

The hardest part was getting the model to give a complete answer and point to the right source. During testing, the PIN answer left out some steps, and the VPN answer pointed to the wrong excerpt. I learned that finding useful text does not always mean the model will use it correctly. The app did say it could not answer the unrelated question, which was good, but I would need more tests to see how often it gets this right.

If I improve the app later, I would try re-ranking. This means finding more possible matches, then checking which ones best answer the question before sending them to the model. I would run the same questions again to see whether the answers become more complete and the source references improve. I would also check how much longer the app takes to respond.
