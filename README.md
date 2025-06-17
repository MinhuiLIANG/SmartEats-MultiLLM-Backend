## Backend of SmartEats based on Multi-LLM workflow [cui-25-short paper]
This repo includes the backend of a conversational dietary recommender system powered by a multi-LLM workflow. The workflow is pre-defined. The workflow looks like this:

![image](MainFigure.png) 

**🍱 The entrance of this project is `/Central/apifilesm.py`**

**🍝 The project structure is described as follows:**
- `Central`: apis connecting to the frontend;
- `Controllers`: integrating components to form functions;
- `Components` & `Upgrades`: LLM units;
- `DAO`: crud functions connecting to the database;
- `fixedSentences.py`: pre-defined sentences;
- `topicTreesm.py`: a tree structure for interaction flow control.

**🥠 What you need to configure:**
- OpenAI api-key;
- Firebase credentials under `/DAO`;
- Database urls in `/DAO/dbops.py`.
