## Backend of SmartEats based on Multi-LLM workflow

**The entrance of this project is /Central/apifilesm.py**

**The project structure is described as follows:**
- Central: apis connecting to the frontend;
- Controllers: integrating components to form functions;
- Components: LLM units;
- DAO: crud functions connecting to the database;
- fixedSentences.py: pre-defined sentences;
- topicTreesm: a tree structure for interaction flow control.

**What you need to configure:**
- OpenAI api-key;
- Firebase credentials under /DAO;
- Database urls in /DAO/dbops.
