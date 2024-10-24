<div align="center">
  <h1>
    <br/>
    <img src="img/ethos_sentinel_logo.jpg" alt="Ethos Sentinel" width="60"/>
    <br/>
    Ethos Sentinel
  </h1>
</div>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3120/">
    <img src="https://img.shields.io/badge/python-3.12.0-blue.svg"/>
  </a>
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/dependency-poetry-%B2EA00"/>
  </a>
  <a href="https://github.com/qhreul/langchain-util/blob/develop/LICENSE">
    <img src="https://img.shields.io/pypi/l/giteo"/>
  </a>
</p>

- [Description](#description)
- [Development](#development)
  - [Requirements](#requirements)
  - [Environment Variables](#environment-variables)
  - [How to prepare the environment](#how-to-prepare-the-environment) 

## Description <a name="description"></a>
The [Responsible AI dashboard](https://learn.microsoft.com/en-us/training/modules/train-model-debug-with-responsible-ai-dashboard-azure-machine-learning/) 
is built on the latest open-source tools developed by the leading academic institutions and organizations including 
Microsoft. These tools are instrumental for data scientists and AI developers to better understand model behavior, 
discover and mitigate undesirable issues from AI model using ErrorAnalysis, InterpretML, Fairlearn, DiCE, and EconML.

Assessing and debugging machine learning models is critical for model reliability, interpretability, fairness, 
and compliance. It helps determine how and why AI systems behave the way they do. You can then use this knowledge to 
improve model performance. Conceptually, model debugging consists of three stages:

<img src="img/model-debugging.png" alt="Model Debugging" width="600"/>

## Development <a name="development"></a>

### Requirements <a name="requirements"></a>
* Git
* Python >= 3.11
* Poetry >= 1.7.0

### Environment Variables <a name="environment-variables"></a>
| **Name**               | **Description**                                    | **Default**     |
|------------------------|----------------------------------------------------|-----------------|
| `LOG_DIR`              | Location of the logging files                      | logs/           |
| `LOG_LEVEL`            | Logging level to be applied during execution       | INFO            |

### How to prepare the environment <a name="how-to-prepare-the-environment"></a>
* Install dependencies
  ```
  poetry install
  ```
  ---
  **NOTE**
  To update dependencies, it may be needed to run the following command prior to installing the packages:
  ```
  poetry lock
  ```
  ---