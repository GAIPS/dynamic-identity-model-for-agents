# Dynamic Identity Model For Agents

The Dynamic Identity Model for Agents (DIMA) is grounded on the Social Identity Approach (SIA), aiming to provide agents with multi-faceted and context-dependent identities. At the core of the model is the identity salience mechanism, which uses agents’ perceived information regarding their social environment to determine the salience of social identities. Agents can then define their identities as unique individuals (personal identity) or as members of a social group (social identity). Consequently, each agent’s active identity will regulate their decisions in a given situation. This model can be integrated in a standard social agent architecture with a perception and decision-making modules.

Details about the model formalization and implementation can be found in the <i>JupyterNotebook</i> folder, in the <i>DynamicIdentityModelForAgents.ipynb</i> file. In addition, this folder contains two files showing how to configure DIMA for specific simulation scenarios, the <i>DIMA_TrashCollection.ipynb</i>, in which it's possible to see the impact of adding the DIMA module in a trash collection scenario, and the <i>DIMA_DictatorGame.ipynb</i> file, in which several Dictator Game experiments are executed given different configurations of the social context. The plots resulting from these experiments can be found in <i>JupyterNotebook/DIMA_plots</i> (<b>Note</b>: in a recent update, we changed the code to add markers to the scenario plots in case plot lines overlapped). 

# DIMA Process Diagram
<img src="https://github.com/GAIPS/dynamic-identity-model-for-agents/blob/main/JupyterNotebook/DIMA_figures/dima.png?raw=true" width=600>

# DIMA Integration in Social Agent Architecture
<img src="https://github.com/GAIPS/dynamic-identity-model-for-agents/blob/main/JupyterNotebook/DIMA_figures/dimaModel_agentElements.png?raw=true" width=600>

# Getting Started
- Learning about the model and playing with the scenario
1. Download or clone this repository
2. If you're not familiar with Jupyter Notebook, follow this tutorial: https://www.dataquest.io/blog/jupyter-notebook-tutorial/
3. Explore the Jupyter Notebook files (run the scenarios, change parameters, understand the formalization, and so on)

As a final remark, we also provide a Python implementation of the model, in case one would like to include DIMA's identity salience mechanism in their own model and, consequently, enhance their agents' realism. Before using/changing this Python application, we advise you to clearly understand the model formalization and setup, given the Jupyter Notebook step-by-step explanation.
