# JavaScript Coding Guidelines

## 1. Naming Convention

Use camelCase for variables and functions.

Examples:

Correct:
getUserData()
loginStatus
userName

Incorrect:
get_user_data()

Rules:

- Must start with a letter, _ , or $
- Cannot start with a number
- No spaces allowed

Valid examples:

name
_user
$total

Invalid examples:

1name
9user

Example:

❌ let user name = "code";

✔ let userName = "code";

---

## 2. Reserved Keywords

Reserved words cannot be used as variable names.

Invalid:

let class = "A"
let return = 5
let function = 10

Correct:

let classId = "A"
let returnValue = 5

Common reserved words:

if  
else  
for  
while  
return  
class  
function  
new  
let  
var  
const  
try  
catch

---

## 3. Code Readability

Code should be:

- Easy to understand
- Self explanatory
- Use meaningful variable names

Example:

Good:

let totalPrice

Bad:

let tp

---

## 4. Comments

Comments should explain **WHY** the logic exists, not HOW the code works.

---

## 5. Reusability & Single Responsibility

Each function should do **only one task**.

Avoid very large functions.

---

## 6. Security & Testing

- Always validate user input
- Write unit tests
- Avoid unsafe operations