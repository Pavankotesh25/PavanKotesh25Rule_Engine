# PavanKotesh25Rule_Engine
Developed a dynamic rule engine that utilizes an Abstract Syntax Tree (AST) to create, combine, and evaluate conditions. The system determines user eligibility based on attributes such as age, department, and income. It features a simple UI, API endpoints, and backend components, with rules stored in an SQLite database. The schema supports dynamic rule changes, and rules are combined using logical operators like AND/OR for efficient evaluations.

The project is structured using a 3-tier architecture: user interface, API layer, and backend. The user interface allows for easy rule creation and management, while the API layer processes rules into AST nodes. The backend evaluates the rules based on user data, and SQLite handles data storage for its simplicity and easy integration.

Key functionalities include dynamic rule creation via AST, recursive condition evaluation, and rule modification. The system features robust error handling to manage invalid rule strings or data formats. Dependencies include Python 3.x, requests, matplotlib, and sqlite3, listed in a requirements.txt file for easy installation.

To start, clone the repository, install the dependencies, and run the application using Python. Setup instructions and design details are provided in the README.md file. The project is open-source under the MIT License, welcoming further contributions.

The rule engine’s use of AST provides flexibility and scalability, making it efficient for handling complex conditions. SQLite ensures persistent data storage, allowing for seamless rule management and evaluation.

Python Script Output Results:

TEST CASE 1: Create individual rules and verify AST representation.

Rule 1 AST: (>, 'age', '30') AND (==, 'department', 'Sales')
Rule 2 AST: (>, 'salary', '50000') OR (>, 'experience', '5')
Rule 3 AST: (<, 'age', '25') AND (==, 'department', 'Marketing')

TEST CASE 2: Combine rules and verify the combined AST.

Combined AST (AND): ((((age > 30) AND (department == 'Sales')) AND ((salary > 50000) OR (experience > 5))) AND ((age < 25) AND (department == 'Marketing')))
Combined AST (OR): ((((age > 30) AND (department == 'Sales')) OR ((salary > 50000) OR (experience > 5))) OR ((age < 25) AND (department == 'Marketing')))

TEST CASE 3: Test evaluate_rule with sample JSON data for different scenarios.

User eligibility (AND): False
User eligibility (OR): True
New data eligibility (AND): False
New data eligibility (OR): True

TEST CASE 4: Explore combining additional rules and test invalid rule functionality.

Invalid rule test: TypeError - Invalid comparison between int and str
Evaluation result for invalid rule: False
