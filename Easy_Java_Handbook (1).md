# The Ultimate Java Placement Handbook (Easy-to-Understand Edition)

*A simple, beginner-friendly Java guide for placements and interviews — explained in plain language, with examples and real-life comparisons. Covers everything from basics to Modern Java (up to Java 25).*

---

## How to Use This Handbook

- If you are a **beginner**, read it from Part 1 to the end, in order.
- If you have an **interview tomorrow**, jump to Part 16 (Top Interview Questions) and Part 17 (Common Mistakes).
- Every topic is explained the same simple way:
  1. **What it means** (in plain words)
  2. **Why it exists / why it matters**
  3. **A simple example**
  4. **Interview questions** you might be asked
  5. **Mistakes people commonly make**

You don't need to memorize anything — just understand the *idea* behind each topic, and the code will make sense naturally.

---

## Table of Contents

1. Java Basics — What is Java and how does it work?
2. Strings
3. Arrays & Methods
4. Object-Oriented Programming (OOP)
5. Exception Handling (Error Handling)
6. Collections Framework (Lists, Sets, Maps)
7. Generics
8. Multithreading & Concurrency
9. File Handling
10. Interfaces, Abstract Classes, Inner Classes & Enums
11. Annotations & Reflection
12. Design Patterns
13. JVM, Memory & Garbage Collection
14. Modern Java Features (Java 8 to Java 25)
15. Coding Patterns for Interviews
16. Top Interview Questions
17. Common Mistakes
18. Cheat Sheets
19. Final Revision Plan & Glossary

---

# Part 1: Java Basics

> **📌 Definition:** Java is a high-level, class-based, object-oriented, platform-independent programming language that compiles to bytecode and runs on the JVM.
>
> **Main points interviewers expect you to know:**
> - Compile → bytecode (`.class`) → JVM interprets/JIT-compiles it → runs on any OS ("Write Once, Run Anywhere").
> - JDK (write + run) ⊃ JRE (run only) ⊃ JVM (the engine itself).
> - 8 primitive types vs reference types; primitives are NOT objects, so Java isn't 100% object-oriented.
> - Stack stores method calls/local variables (fast, temporary); Heap stores objects (slower, garbage-collected).
> - Local variables need a manual initial value; fields get automatic defaults.
> - `==` compares references/addresses; `.equals()` compares content.

## 1.1 What is Java? (In Simple Words)

Think of Java like a **universal language** for computers. Normally, if you write a program for Windows, it won't run on Mac or Linux without changes — the languages "speak" differently to each operating system.

Java solves this problem. You write your code **once**, and it can run on **any device** — Windows, Mac, Linux, Android — without rewriting anything. This is Java's famous slogan: **"Write Once, Run Anywhere" (WORA)**.

**Formal Definition:** Java is a high-level, object-oriented, platform-independent programming language.

- **High-level** → it reads almost like English, not like raw machine instructions.
- **Object-oriented** → it organizes code around real-world "things" (objects), like a `Car`, a `Student`, a `BankAccount`.
- **Platform-independent** → the same compiled code runs on any operating system.

## 1.2 How Does Java Actually Run? (Step by Step)

This confuses a lot of beginners, so let's go slow.

1. You write your code in a file like `HelloWorld.java`. This is plain, human-readable text.
2. You **compile** it using a tool called `javac` (Java Compiler). This converts your code into something called **bytecode**, saved as `HelloWorld.class`. Bytecode is NOT the same as the machine code your computer understands directly — it's a "middle" language.
3. This bytecode is given to the **JVM (Java Virtual Machine)** — a program installed on your computer that knows how to read bytecode.
4. The JVM translates the bytecode into instructions your specific computer's processor understands, and runs the program.

**Why does this two-step process exist?**
Because the bytecode is the SAME on every computer — only the JVM is different for each operating system. So as long as a computer has a JVM installed, it can run your Java program, no matter what OS it is.

```
Your Code (HelloWorld.java)
        ↓  [Compiled by javac]
Bytecode (HelloWorld.class)  ← same on every computer
        ↓  [Read by JVM — different for each OS]
Runs on your computer
```

**A simple example:**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Placement!");
    }
}
```

What's happening here:
- `public class HelloWorld` → we are creating a "blueprint" called `HelloWorld`.
- `public static void main(String[] args)` → this is the special starting point. Every Java program begins execution here. Think of it as the "front door" the JVM walks through first.
- `System.out.println(...)` → this simply prints text to the screen.

## 1.3 JVM Architecture (Simple Explanation)

Since we just mentioned the JVM, let's peek inside. The Java Virtual Machine (JVM) is the engine that runs your Java programs. It consists of three main parts:

1. **Class Loader Subsystem**: Its job is to read your compiled `.class` files (bytecode) and load them into memory when they are needed.
2. **Runtime Data Areas (Memory)**: This is the memory space where Java stores everything while running. The most important areas are the **Heap** (where objects live) and the **Stack** (where method calls and local variables live). We will discuss these more later.
3. **Execution Engine**: This is the part that actually runs the code. It has three main helpers:
   - **Interpreter**: Reads the bytecode line by line and executes it (can be a bit slow).
   - **JIT (Just-In-Time) Compiler**: Watches for code that runs over and over again, and compiles it directly into lightning-fast machine code to speed things up.
   - **Garbage Collector**: Automatically cleans up unused objects to free memory.

## 1.4 JDK vs JRE vs JVM — The Most Asked Beginner Question

This trips up almost everyone at first, so here's a simple analogy:

Imagine you want to **cook a meal**.
- **JVM** = the stove. It's the actual engine that "runs" things.
- **JRE** = the kitchen with the stove and basic ingredients — enough to cook and eat a meal someone already prepared. (You can *run* food, but not *create new recipes*.)
- **JDK** = the full kitchen PLUS recipe books, knives, and tools to actually create new dishes. (You can both *write* and *run* programs.)

| Term | What it does | Who needs it |
|---|---|---|
| **JVM** (Java Virtual Machine) | Actually runs your bytecode | Anyone running a Java app |
| **JRE** (Java Runtime Environment) | JVM + libraries needed to run programs | Someone who only wants to *run* Java apps, not write code |
| **JDK** (Java Development Kit) | JRE + the compiler (`javac`) and developer tools | Programmers — anyone *writing* Java code |

**Simple rule to remember:** JDK contains JRE, and JRE contains JVM. So if you install the JDK (which developers always do), you automatically get everything.

## 1.5 Variables and Data Types — Explained Simply

A **variable** is just a labeled box that stores a value. You give it a name, and you put something inside it.

```java
int age = 25;      // a box named "age" holding the number 25
String name = "Tom"; // a box named "name" holding the text "Tom"
```

Java has 2 categories of types:

**1. Primitive types** — these are the 8 simplest, most basic types. They directly hold a value, nothing fancy.

| Type | What it stores | Example |
|---|---|---|
| `byte` | A very small whole number | `byte b = 10;` |
| `short` | A small whole number | `short s = 1000;` |
| `int` | A normal whole number (most commonly used) | `int x = 50000;` |
| `long` | A very large whole number | `long big = 10000000000L;` |
| `float` | A decimal number (less precise) | `float f = 3.14f;` |
| `double` | A decimal number (more precise, default choice) | `double d = 3.14159;` |
| `char` | A single character | `char c = 'A';` |
| `boolean` | True or false only | `boolean isReady = true;` |

**2. Reference types** — these are everything else: `String`, arrays, objects you create, etc. Instead of storing the actual value directly, a reference type variable stores the **address/location** of where the real data lives in memory.

**Why does this distinction matter?** Because it affects how copying works. If you copy a primitive variable, you get an independent copy. If you copy a reference variable, both variables point to the **same** object — so changing one can affect the other (we'll see this in detail in the OOP and Methods sections).

> **Beginner trap:** Local variables (declared inside a method) do NOT get a default value automatically — you must assign one yourself, or the code won't compile. But fields (variables declared inside a class, outside any method) DO get automatic default values (`0` for numbers, `false` for boolean, `null` for objects).

## 1.6 Stack vs Heap — Where Does Data Actually Live?

Imagine your computer's memory as having two separate areas:

**The Stack** — like a stack of plates. Every time you call a method, a new "plate" (called a stack frame) is added on top, holding that method's local variables. When the method finishes, its plate is removed. Fast, but temporary and limited in size.

**The Heap** — like a big warehouse. This is where actual **objects** live (anything created with `new`). Objects stay here until nothing refers to them anymore, at which point Java's automatic cleanup system (Garbage Collector) removes them. Larger, but a bit slower to access than the stack.

| | Stack | Heap |
|---|---|---|
| What it stores | Method calls and local variables | Objects (created with `new`) |
| Lifetime | Disappears when the method ends | Lives until garbage collected |
| Speed | Faster | Slower |
| Error if full | `StackOverflowError` (e.g. infinite recursion) | `OutOfMemoryError` |

## 1.7 Interview Questions for This Part

**Q1: What are the main features of Java?**
A: Simple to learn, Object-Oriented, Platform-Independent, Secure, Robust (handles errors well), supports Multithreading, and has good Performance through something called the JIT compiler (it speeds up frequently-used code at runtime).

**Q2: Is Java fully object-oriented?**
A: Not 100%. The 8 primitive types (`int`, `boolean`, etc.) are NOT objects — they're kept simple and lightweight for performance reasons.

**Q3: What's the difference between JDK, JRE, and JVM?**
A: See the kitchen analogy above — JDK is for developers (write + run), JRE is for running already-written apps, JVM is the actual engine.

**Q4: What's the difference between `==` and `.equals()`?**
A: `==` checks if two variables point to the exact same object in memory. `.equals()` checks if the *content* inside two objects is the same, even if they are different objects. We'll explore this more in the Strings section.

## 1.8 Common Mistakes Beginners Make

- Thinking **Java and JavaScript** are related because of the similar name — they are completely different languages with different purposes.
- Forgetting that a local variable **must** be given a value before you use it (the compiler will give an error otherwise).
- Confusing `==` (comparing memory addresses for objects) with `.equals()` (comparing actual content).


---

# Part 2: Strings

> **📌 Definition:** A `String` is an immutable sequence of characters; once created, its content can never change — any "modification" creates a new object.
>
> **Main points interviewers expect you to know:**
> - Why String is immutable: security, thread safety, hashcode caching for fast `HashMap` keys.
> - The String Pool: literals are reused/shared; `new String()` always forces a separate heap object.
> - `==` vs `.equals()` for Strings — the #1 trap.
> - `String` (immutable) vs `StringBuilder` (mutable, fast, single-threaded) vs `StringBuffer` (mutable, thread-safe, slower).
> - Why concatenating in a loop with `+` is wasteful — use `StringBuilder`.

## 2.1 What is a String? (In Simple Words)

A `String` is just text — a sequence of characters, like `"Hello"` or `"Java123"`. It's one of the most-used types in Java.

The most important thing to understand about Strings: **they are immutable**, which means once you create a String, you can never change its content. Every time you "modify" a string, Java secretly creates a **brand new** String object behind the scenes, and your variable just starts pointing to that new one.

```java
String name = "Tom";
name = name + " Smith";  // this does NOT change the original "Tom" string.
                           // Instead, Java creates a NEW string "Tom Smith"
                           // and "name" now points to that new one.
```

## 2.2 The String Pool — Why Strings Behave Strangely Sometimes

Java has a special memory area called the **String Pool** (or String Constant Pool), used purely to save memory.

Here's the idea: if your program uses the text `"hello"` in five different places, why should Java store five separate copies of the exact same text? Instead, Java keeps just ONE copy in the String Pool, and every variable that uses the literal `"hello"` simply points to that same shared copy.

```java
String a = "hello";              // "hello" is placed in the String Pool
String b = "hello";              // "b" reuses the SAME object as "a" (no new copy made)
System.out.println(a == b);      // true — they point to the exact same object

String c = new String("hello");  // forces a brand NEW object, OUTSIDE the pool, on the heap
System.out.println(a == c);      // false — different objects, even though content is identical
System.out.println(a.equals(c)); // true — content is the same
```

**This is the #1 String interview trap** — always remember: `==` checks "are these the literal same object in memory?" while `.equals()` checks "do these have the same content?" For Strings, always use `.equals()` unless you have a specific reason not to.

**Why is String immutable in the first place?** A few good reasons:
- **Security:** Strings are used everywhere — file names, network addresses, passwords. If they could be changed after creation, a malicious piece of code could secretly alter them.
- **Thread safety:** Since the content never changes, multiple parts of your program (even running at the same time) can safely share the same String without any risk of conflicts.
- **Speed:** Java can calculate the "hashcode" of a string once and remember it forever, making Strings very fast to use as keys in things like `HashMap`.

## 2.3 String vs StringBuilder vs StringBuffer

Since Strings can't be changed, what if you need to build a long piece of text gradually, like inside a loop? Using regular `String` for this is slow and wasteful, because **every single concatenation creates a brand new String object**.

That's where `StringBuilder` comes in — it's a **mutable** (changeable) version of a String, designed exactly for this purpose.

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 5; i++) {
    sb.append(i);   // modifies the SAME object each time, instead of creating new ones
}
System.out.println(sb.toString());  // 01234
```

| | `String` | `StringBuilder` | `StringBuffer` |
|---|---|---|---|
| Can change after creation? | No (immutable) | Yes (mutable) | Yes (mutable) |
| Safe to use across multiple threads? | Yes (because it never changes) | No | Yes (it locks itself while being modified) |
| Speed | Slow if you keep modifying it | Fast | Slightly slower than StringBuilder (because of the locking) |
| When to use | Text that doesn't change much | Building/editing text in a single-threaded program (most common case) | Building/editing text shared across multiple threads |

**Simple rule:** Use `StringBuilder` by default when building strings in a loop. Only reach for `StringBuffer` if multiple threads will modify the same string builder at the same time (rare in practice).

## 2.4 Useful String Methods (Quick Reference)

| Method | What it does |
|---|---|
| `length()` | tells you how many characters are in the string |
| `charAt(i)` | gives you the character at a specific position |
| `substring(start, end)` | cuts out a piece of the string |
| `equals()` | compares the actual text content of two strings |
| `split(",")` | breaks a string apart into a list, using a separator |
| `trim()` / `strip()` | removes extra spaces from the start/end |
| `toUpperCase()` / `toLowerCase()` | changes the case of letters |
| `isBlank()` (Java 11+) | checks if a string is empty or only contains spaces |
| `repeat(n)` (Java 11+) | repeats the string `n` times |

## 2.5 Interview Questions

**Q1: Why is String immutable in Java?**
A: For security (can't be secretly changed), thread safety (safe to share across threads), and performance (its hashcode can be cached once and reused).

**Q2: How many objects does `new String("abc")` create?**
A: Two — one for the literal `"abc"` that goes into the String Pool, and another separate object created on the heap by the `new` keyword.

**Q3: Why use StringBuilder instead of String in a loop?**
A: Because regular String concatenation creates a brand-new object on every single iteration, which wastes memory and is slow. StringBuilder modifies one object in place.

## 2.6 Common Mistakes

- Comparing strings with `==` instead of `.equals()` — this can give you wrong/unexpected results.
- Using `+` to build strings inside a loop instead of `StringBuilder`.
- Assuming that `.trim()`, `.toUpperCase()`, etc. change the original string — they don't; they always return a brand NEW string, and you must save it into a variable to keep it.


---

# Part 3: Arrays & Methods

> **📌 Definition:** An array is a fixed-size, ordered container of values of the same type; a method is a named, reusable block of code with a defined input/output contract.
>
> **Main points interviewers expect you to know:**
> - Arrays have fixed size and 0-based indexing; out-of-range access throws `ArrayIndexOutOfBoundsException`.
> - Java is always **pass-by-value** — for objects, the reference's value (not the object) is copied.
> - Method **overloading** = same name, different parameters, same class, resolved at compile time.
> - Method **overriding** = subclass redefines a parent method, resolved at runtime (polymorphism).
> - `array.length` (property) vs `string.length()`/`list.size()` (methods).

## 3.1 Arrays — Explained Simply

Imagine you need to store 100 student marks. Creating 100 separate variables (`mark1`, `mark2`, ... `mark100`) would be painful. An **array** lets you store many values of the same type, together, under one name.

```java
int[] marks = new int[5];          // creates an array that can hold 5 integers, all starting at 0
int[] scores = {90, 85, 70, 60, 95}; // creates an array directly with these 5 values

System.out.println(scores[0]);     // 90 (arrays start counting from index 0, not 1!)
System.out.println(scores.length); // 5 (the total number of items)
```

**Things to remember about arrays:**
- The size is **fixed** once created — you can't add a 6th item to a 5-item array. (If you need a flexible size, use an `ArrayList` instead — covered in Part 6.)
- Counting starts at **index 0**, not 1. The last item's index is `length - 1`.
- Trying to access an index that doesn't exist (like `scores[10]` on a 5-item array) throws an `ArrayIndexOutOfBoundsException` — a very common beginner bug.
- Arrays are themselves objects in Java, stored on the heap.

## 3.2 Methods — Explained Simply

A **method** is a reusable, named block of code that does one specific task. Instead of writing the same logic over and over, you write it once as a method, and call it whenever you need it.

```java
public int add(int a, int b) {
    return a + b;
}
// usage:
int result = add(5, 3);  // result = 8
```

**Breaking this down:**
- `public` → who can access this method (we'll cover access modifiers more in OOP).
- `int` → the type of value this method gives back (its "return type").
- `add` → the name of the method.
- `(int a, int b)` → the inputs (called "parameters") the method needs to do its job.
- `return a + b;` → sends the result back to whoever called the method.

## 3.3 Is Java "Pass-by-Value" or "Pass-by-Reference"? (A Tricky but Important Concept)

This is one of the most misunderstood topics, so let's go very slowly.

**Java is ALWAYS pass-by-value.** This means: when you pass a variable into a method, Java copies the *value* of that variable into the method's parameter.

- For **primitives** (`int`, `double`, etc.), the actual number is copied. Changing the parameter inside the method has zero effect on the original variable.
- For **objects** (anything created with `new`), what gets copied is the **reference** (the "address" pointing to where the object lives) — NOT the object itself. So both the original variable and the method's parameter now point to the *same* object. This means:
  - You CAN change the object's internal data through the parameter (because both point to the same real object).
  - You CANNOT make the original variable point to a *different* object by reassigning the parameter inside the method.

```java
void changeValue(int x) {
    x = 100;   // only changes the LOCAL copy — has no effect outside this method
}

void changeName(StringBuilder sb) {
    sb.append(" Smith"); // this DOES affect the original object, because both
                          // variables point to the same StringBuilder in memory
}

void reassign(StringBuilder sb) {
    sb = new StringBuilder("New Object"); // this does NOT affect the original variable —
                                            // it just makes the LOCAL copy point elsewhere
}
```

## 3.4 Method Overloading vs Method Overriding

These two sound similar but are completely different concepts.

**Overloading** — having multiple methods with the **same name**, but different parameters, **within the same class**. Java figures out which one to use based on what arguments you pass.

```java
void print(int x) { }
void print(String x) { }
void print(int x, int y) { }
```

**Overriding** — when a **subclass** provides its OWN version of a method that already exists in its **parent class**, using the exact same name and parameters. This lets the subclass customize behavior.

```java
class Animal {
    void sound() { System.out.println("Some generic sound"); }
}
class Dog extends Animal {
    @Override
    void sound() { System.out.println("Bark!"); }  // overrides the parent's version
}
```

| | Overloading | Overriding |
|---|---|---|
| Where it happens | Same class, multiple versions of one method | Parent class and child class |
| Decided when? | At compile time (Java knows which version to call just by looking at your code) | At runtime (Java checks the actual object type while the program is running) |
| Purpose | Convenience — same action name, different inputs | Customization — child class changes/specializes parent behavior |

## 3.5 Interview Questions

**Q1: Is Java pass-by-value or pass-by-reference?**
A: Always pass-by-value. For objects, what's "passed by value" is the reference (memory address) itself — not the actual object.

**Q2: Difference between overloading and overriding?**
A: Overloading = same method name, different parameters, in the SAME class (decided at compile time). Overriding = subclass redefines the parent's exact method (decided at runtime).

**Q3: What happens if you access an array index that doesn't exist?**
A: You get an `ArrayIndexOutOfBoundsException` — a runtime error.

## 3.6 Common Mistakes

- Thinking Java passes objects "by reference" in the same way as C++ — it doesn't; only the reference's *value* is copied.
- Forgetting array indices start at 0.
- Confusing `array.length` (no parentheses, it's a property) with `string.length()` (a method, needs parentheses) and `list.size()` (also a method).


---

# Part 4: Object-Oriented Programming (OOP)

> **📌 Definition:** OOP is a programming paradigm that models software as interacting "objects" — bundles of data (fields) and behavior (methods) — built on four pillars: Encapsulation, Inheritance, Polymorphism, and Abstraction.
>
> **Main points interviewers expect you to know:**
> - **Encapsulation** — hide data, expose controlled access via getters/setters.
> - **Inheritance** — `extends` reuses parent code; single inheritance only for classes.
> - **Polymorphism** — dynamic method dispatch: the actual object type (not the declared type) decides which overridden method runs, at runtime.
> - **Abstraction** — hide implementation details, expose only what's necessary (`abstract` classes, interfaces).
> - Constructors initialize objects; can be overloaded; `this(...)` chains constructors.
> - `equals()`/`hashCode()` contract — must override together or break `HashMap`/`HashSet`.
> - `static` = belongs to the class, not an instance; `final` = cannot be changed/overridden/extended.
> - Abstract class vs interface — single vs multiple inheritance, shared code vs pure contract.

## 4.1 What is OOP, Really?

Object-Oriented Programming means organizing your code around **real-world things (objects)** instead of just a list of instructions. Think of a `Car` — it has properties (color, speed, brand) and behaviors (start, stop, accelerate). In OOP, we model this directly in code:

```java
class Car {
    String color;       // property
    void start() { }     // behavior
}
```

OOP is built on **four core ideas**. Let's explain each one simply, with an analogy.

## 4.2 Pillar 1: Encapsulation

**Simple idea:** Bundling data (variables) and methods together, while keeping the object's internal data hidden (private). You only allow controlled access through specific methods called **getters** and **setters**. This is also known as **data hiding**.

**Analogy:** Think of a medicine capsule. The medicine (data) is hidden safely inside the shell (methods). Or think of an ATM machine: you can't directly reach in and grab cash from the vault — you must go through the proper interface (insert card, enter PIN, choose amount). The machine controls and validates everything.

**Access Modifiers:**
Java provides 4 levels of access control:
1. `private`: Accessible ONLY within the same class (perfect for fields).
2. `default` (no keyword): Accessible within the same package.
3. `protected`: Accessible within the same package AND by subclasses (even in other packages).
4. `public`: Accessible from anywhere.

```java
public class BankAccount {
    private double balance;   // hidden (data hiding) — nobody outside can touch this directly

    // Getter — controlled "read" access
    public double getBalance() { 
        return balance; 
    }  
    
    // Setter — controlled "write" access with validation
    public void deposit(double amount) {
        if (amount > 0) {       // validation happens here, safely
            balance += amount;  
        }
    }
}
```

**Why it matters:** It protects your object from being put into an invalid state (e.g., setting a negative balance), and it lets you change the internal code later without breaking the rest of the application that uses your class.

## 4.3 Pillar 2: Inheritance

**Simple idea:** A class can "inherit" properties and behaviors from another class, so you don't have to rewrite the same code.

**Analogy:** A `Dog` is a kind of `Animal`. All animals can eat and sleep — a Dog doesn't need to redefine those; it just adds its own special behavior, like barking.

```java
class Animal {
    void eat() { System.out.println("Eating..."); }
}
class Dog extends Animal {       // Dog inherits everything from Animal
    void bark() { System.out.println("Barking..."); }
}
// A Dog object can now both eat() AND bark()
```

**Important rule:** A Java class can only inherit from **one** parent class (`extends`), to avoid confusing situations where two parents might have conflicting versions of the same method. But a class CAN implement multiple **interfaces** (more on this in Part 10).

## 4.4 Pillar 3: Polymorphism

**Simple idea:** "Poly" = many, "morph" = forms. The same action can behave differently depending on which object is actually performing it.

**Analogy:** Pressing "play" on a music app, a video app, and a game does different things — but it's the same button/action conceptually.

```java
class Animal {
    void sound() { System.out.println("Some sound"); }
}
class Dog extends Animal {
    void sound() { System.out.println("Bark"); }
}
class Cat extends Animal {
    void sound() { System.out.println("Meow"); }
}

Animal a = new Dog();
a.sound();   // prints "Bark" — even though "a" is declared as type Animal,
              // Java checks the ACTUAL object at runtime and calls Dog's version
```

This is called **dynamic method dispatch** — Java decides which version of the method to actually run based on the real object, not the variable's declared type. This happens at runtime, which is why it's also called "runtime polymorphism."

## 4.5 Pillar 4: Abstraction

**Simple idea:** Hide the complicated details, and only show what's necessary.

**Analogy:** When you drive a car, you press the accelerator without knowing exactly how the engine internally combusts fuel. The car "abstracts away" that complexity.

```java
abstract class Shape {
    abstract double area();   // no body — just a promise that subclasses MUST implement this
}
class Circle extends Shape {
    double radius;
    double area() { return Math.PI * radius * radius; }  // actual implementation
}
```

## 4.6 Constructors — How Objects Are Created

A **constructor** is a special method, automatically called when you create a new object with `new`, used to set up its initial state.

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {   // constructor — same name as the class, no return type
        this.name = name;
        this.age = age;
    }
}
Person p = new Person("Alice", 30);  // this calls the constructor automatically
```

- If you don't write any constructor yourself, Java automatically gives you a free, empty one (called the "default constructor").
- You can have multiple constructors with different parameters — this is called **constructor overloading**.
- `this(...)` lets one constructor call another constructor in the same class — useful to avoid repeating setup code.

## 4.7 `equals()` and `hashCode()` — Why They Go Together

By default, `equals()` just checks if two variables point to the exact same object (basically the same as `==`). Often, you want it to instead check if two objects have the *same content* — like two `Person` objects with the same name and age being considered "equal" even though they're technically different objects.

```java
class Person {
    String name;
    int age;

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Person p)) return false;
        return age == p.age && name.equals(p.name);
    }
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

**Why must you ALWAYS override both together?** Java has a rule: if two objects are `.equals()`, they MUST also have the same `hashCode()`. This rule is crucial because things like `HashMap` and `HashSet` use `hashCode()` to quickly find where an object should be stored — if you break this rule, your objects will behave unpredictably when stored in these collections (e.g., a `HashSet` might allow duplicate "equal" objects, or fail to find an object that's clearly inside it).

## 4.8 `static` and `final` — Two Important Keywords

**`static`** means "this belongs to the class itself, not to any individual object." Imagine a school: each student has their own name, but there's only one shared "school name" — that's what `static` represents.

```java
class Student {
    static String schoolName = "ABC High School";  // shared by ALL Student objects
    String name;                                     // unique to each Student object
}
```

**`final`** means "this cannot be changed once set."
- On a variable → it becomes a constant (can't be reassigned).
- On a method → it can't be overridden by a subclass.
- On a class → it can't be extended/subclassed at all (e.g., `String` is a `final` class).

## 4.9 Interview Questions

**Q1: What is dynamic method dispatch?**
A: It's how Java decides, at runtime, which actual version of an overridden method to run — based on the real object, not the declared variable type.

**Q2: Difference between an abstract class and an interface?**

| | Abstract Class | Interface |
|---|---|---|
| Can have regular (working) methods? | Yes | Yes (since Java 8, via `default` methods) |
| Can have unfinished ("abstract") methods? | Yes | Yes |
| Can a class inherit from multiple of these? | No (only one abstract class) | Yes (a class can implement many interfaces) |
| When to use | When subclasses share a lot of common code | When you just want to define a "capability" or contract |

**Q3: Why must `equals()` and `hashCode()` always be overridden together?**
A: Because hash-based collections like `HashMap` rely on this consistency to correctly find and compare objects (see section 4.7).

**Q4: Can a constructor be private? Why would you do that?**
A: Yes — this is commonly used in the Singleton design pattern (Part 12), where you want to guarantee only one instance of a class ever exists.

## 4.10 Common Mistakes

- Overriding `equals()` but forgetting to also override `hashCode()` — this silently breaks `HashMap`/`HashSet` behavior.
- Believing a `static` method can be "overridden" the same way as a regular method — it can only be "hidden," because static methods aren't polymorphic.
- Forgetting that Java only allows single inheritance for classes (one `extends` only).


---

# Part 5: Exception Handling (Error Handling)

> **📌 Definition:** An exception is an object representing an abnormal event during program execution; exception handling lets you anticipate and respond to errors instead of crashing.
>
> **Main points interviewers expect you to know:**
> - Hierarchy: `Throwable` → `Error` (unrecoverable) and `Exception` → Checked (compiler-enforced) and `RuntimeException` (unchecked, usually a bug).
> - `try`/`catch`/`finally` semantics; `finally` almost always runs (except `System.exit()` or JVM crash).
> - Try-with-resources auto-closes resources (`AutoCloseable`).
> - Custom exceptions extend `Exception` (checked) or `RuntimeException` (unchecked).
> - `throw` (actually throws an exception now) vs `throws` (declares a method might throw one).

## 5.1 What is an Exception?

When something goes wrong while your program is running — like dividing by zero, or trying to use an object that doesn't exist — Java creates a special object describing the problem, called an **exception**. If you don't handle it, your program crashes and prints an error message (a "stack trace").

**Why do we need a system for this?** Without exception handling, one small error anywhere would crash your entire program immediately. Exception handling lets you anticipate problems and respond gracefully instead of crashing.

## 5.2 The Exception Family Tree

```
Throwable  (the top-level "something went wrong" type)
├── Error            → serious problems, usually unrecoverable (e.g., running out of memory)
└── Exception
    ├── Checked Exceptions     → the compiler FORCES you to handle these
    └── RuntimeException       → "Unchecked" — handling is optional, but usually indicates a bug
```

| Type | Must you handle it? | Examples | What it usually means |
|---|---|---|---|
| **Checked Exception** | Yes — compiler won't let you skip it | `IOException`, `SQLException` | An external, expected problem (e.g., a file might not exist) |
| **Unchecked Exception (RuntimeException)** | No — but you should still fix the underlying bug | `NullPointerException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException` | Usually a programming mistake |
| **Error** | No, and you generally shouldn't try | `OutOfMemoryError`, `StackOverflowError` | Something seriously wrong with the JVM/system itself |

## 5.3 try-catch-finally — The Basic Tool

```java
try {
    int result = 10 / 0;          // this line will throw an exception
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero!");   // this runs if the above fails
} finally {
    System.out.println("This always runs, error or not.");
}
```

- `try` → the code you want to attempt, which might fail.
- `catch` → what to do if a specific type of error happens.
- `finally` → runs no matter what (success or failure) — usually used for cleanup, like closing files.

**Try-with-resources** — a cleaner way to handle things like files that need to be closed afterward, automatically:

```java
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    System.out.println(br.readLine());
}  // br is automatically closed here, even if an error occurred
```

## 5.4 Creating Your Own (Custom) Exceptions

Sometimes Java's built-in exceptions don't describe your specific problem well. You can create your own:

```java
class InsufficientFundsException extends Exception {
    public InsufficientFundsException(String message) {
        super(message);
    }
}

void withdraw(double amount) throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException("Not enough money in account!");
    }
}
```

## 5.5 `throw` vs `throws` — Don't Mix These Up!

| | `throw` | `throws` |
|---|---|---|
| What it does | Actually creates and throws an exception, right now | Just WARNS callers "this method might throw this type of error" |
| Where you write it | Inside the method's body | In the method's signature (the line before `{`) |
| Example | `throw new IllegalArgumentException("Bad input");` | `void readFile() throws IOException { ... }` |

## 5.6 Interview Questions

**Q1: Difference between checked and unchecked exceptions?**
A: Checked exceptions must be either caught or declared (using `throws`) — the compiler enforces this. Unchecked exceptions (RuntimeExceptions) don't require this, and usually represent programming bugs rather than expected, recoverable situations.

**Q2: Can the `finally` block ever be skipped?**
A: Yes, in rare cases — like if `System.exit()` is called, or if the JVM itself crashes.

**Q3: Why is try-with-resources better than manually closing things in `finally`?**
A: It's shorter, less error-prone, and guarantees the resource is closed automatically — even if you forget to write the closing code yourself.

## 5.7 Common Mistakes

- Catching the generic `Exception` type instead of the specific exception, which can hide real bugs you should be fixing.
- Putting a `return` statement inside `finally` — this silently overrides any exception or return value from the `try` block, which is confusing and considered bad practice.
- Forgetting that catching an exception doesn't "undo" the error — your code still needs to handle what happens next logically.


---

# Part 6: Collections Framework (Lists, Sets, Maps)

> **📌 Definition:** The Collections Framework is a unified set of interfaces and classes (`List`, `Set`, `Map`, and their implementations) for storing, retrieving, and manipulating groups of objects.
>
> **Main points interviewers expect you to know:**
> - `List` (ordered, duplicates allowed) vs `Set` (no duplicates) vs `Map` (key-value pairs).
> - `ArrayList` (fast random access, slow middle insert/delete) vs `LinkedList` (fast insert/delete at ends, slow access).
> - `HashMap` internals: hashing → bucket → collision list/tree → resize at 75% load factor.
> - `HashSet`/`HashMap` (no order) vs `LinkedHashSet`/`LinkedHashMap` (insertion order) vs `TreeSet`/`TreeMap` (sorted order).
> - Fail-fast iterators and `ConcurrentModificationException`; use `Iterator.remove()` to modify safely while looping.
> - `Comparable` (one natural order, inside the class) vs `Comparator` (many custom orders, outside the class).
> - Custom objects used as `HashMap`/`HashSet` keys must correctly override `equals()`/`hashCode()`.

## 6.1 What is the Collections Framework?

Arrays are useful, but they have a big limitation: a fixed size, and very few built-in tools to search, sort, or manage data. The **Collections Framework** is a set of ready-made, flexible data structures that solve this — letting you store, search, sort, and organize groups of objects easily.

```
Collection (general idea: "a group of objects")
├── List   → ordered, allows duplicates, like a numbered list           → ArrayList, LinkedList
├── Set    → only unique items, no duplicates allowed                    → HashSet, TreeSet
└── Queue  → items processed in a specific order (usually first-in-first-out) → PriorityQueue

Map → stores key-value pairs (like a dictionary)                         → HashMap, TreeMap
```

## 6.2 List — Ordered, Allows Duplicates

**`ArrayList`** — Think of this like a flexible, resizable array. Great for reading data quickly by position (index), but a bit slower if you're constantly inserting/removing items from the middle.

**`LinkedList`** — Think of this like a chain of connected boxes, where each box knows the next one. Great for frequently adding/removing items, especially at the beginning or end, but slower for random access by index.

```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
System.out.println(names.get(0));  // Alice
```

| | `ArrayList` | `LinkedList` |
|---|---|---|
| Good at | Quickly reading items by position | Quickly adding/removing items at the ends |
| Slower at | Inserting/removing in the middle | Reading items by position |
| When to use | Most common choice — use this by default | When you do LOTS of insertions/deletions |

## 6.3 Set — No Duplicates Allowed

A `Set` is like a `List`, but it automatically rejects duplicate values.

| | `HashSet` | `LinkedHashSet` | `TreeSet` |
|---|---|---|---|
| Order of items | No guaranteed order | Keeps insertion order | Automatically sorted |
| Speed | Fastest | Slightly slower than HashSet | Slower (sorted structure) |
| When to use | When order doesn't matter, just want fast uniqueness | When you want uniqueness AND insertion order preserved | When you want items automatically sorted |

```java
Set<String> uniqueNames = new HashSet<>();
uniqueNames.add("Tom");
uniqueNames.add("Tom");  // ignored — already exists
System.out.println(uniqueNames.size());  // 1
```

## 6.4 Map — Key-Value Pairs (Like a Dictionary)

A `Map` stores data as pairs: a unique **key**, linked to a **value**. Think of a real dictionary — each word (key) has a definition (value).

```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 30);
ages.put("Bob", 25);
System.out.println(ages.get("Alice"));  // 30
```

| | `HashMap` | `LinkedHashMap` | `TreeMap` |
|---|---|---|---|
| Order | No guaranteed order | Keeps insertion order | Automatically sorted by key |
| Speed | Fastest | Slightly slower | Slower (sorted structure) |
| Use case | Default, most common choice | When insertion order matters | When sorted keys matter |

## 6.5 How Does HashMap Actually Work Inside? (Simplified)

This is a very common interview question, so let's break it down simply:

1. When you call `map.put(key, value)`, Java calculates a number from the key called a **hashcode**.
2. This hashcode is used to decide which "bucket" (a small storage slot) the key-value pair goes into. Think of buckets like labeled drawers in a cabinet.
3. Sometimes two different keys produce the same bucket location — this is called a **collision**. When this happens, Java just stores both pairs in that same bucket, in a small internal list.
4. If a bucket somehow gets a LOT of colliding entries (more than 8), Java automatically converts that bucket's internal list into a more efficient structure called a "red-black tree" — making lookups faster in that rare worst-case scenario.
5. If the map gets too full (more than 75% full, by default), Java automatically grows the map bigger and redistributes everything — this is called **resizing/rehashing**.

**Why does this matter?** Because it's why `HashMap` operations are normally extremely fast (close to instant), even with thousands of items — Java is essentially using smart, organized "drawers" instead of searching through everything one by one.

## 6.6 Iterating Safely — The "Fail-Fast" Trap

A very common beginner bug: trying to remove items from a list WHILE looping through it with a normal for-each loop.

```java
// WRONG — this throws a ConcurrentModificationException!
for (String name : names) {
    if (name.equals("Bob")) names.remove(name);
}

// CORRECT — use an Iterator's own remove() method instead
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    if (it.next().equals("Bob")) it.remove();  // safe
}
```

**Why does this happen?** Most collections are "fail-fast" — meaning if they detect they were changed unexpectedly while being looped through, they immediately throw an error rather than letting your program behave unpredictably.

## 6.7 Comparable vs Comparator — Sorting Custom Objects

If you have a list of custom objects (like `Person`), Java doesn't automatically know how to sort them — you need to tell it how.

**`Comparable`** — you build the "default" sorting rule directly INTO the class itself.

```java
class Employee implements Comparable<Employee> {
    int salary;
    public int compareTo(Employee other) {
        return this.salary - other.salary;  // sorts by salary, ascending
    }
}
```

**`Comparator`** — you create a SEPARATE sorting rule, outside the class, useful when you want multiple different ways to sort the same objects.

```java
list.sort(Comparator.comparing(Employee::getSalary).reversed());  // sort by salary, descending
```

| | `Comparable` | `Comparator` |
|---|---|---|
| Where defined | Inside the class itself | Outside, as a separate rule |
| How many sorting orders? | Only one ("natural" order) | As many as you want |
| Use when | There's one obvious, default way to sort | You need flexible/multiple sorting options |

## 6.8 Quick Speed Reference

| Collection | Adding | Removing | Searching | Reading by index |
|---|:---:|:---:|:---:|:---:|
| `ArrayList` | Fast | Slow (in middle) | Slow | Fast |
| `LinkedList` | Fast | Fast (at ends) | Slow | Slow |
| `HashSet` / `HashMap` | Fast | Fast | Fast | — |
| `TreeSet` / `TreeMap` | Medium | Medium | Medium | — |

## 6.9 Interview Questions

**Q1: How does HashMap handle two keys that produce the same hashcode?**
A: It stores both entries in the same "bucket" as a small list (or tree, if the bucket gets too crowded) — see section 6.5.

**Q2: When would you use a `TreeMap` instead of a `HashMap`?**
A: When you need your keys to always stay automatically sorted — at the cost of being a bit slower than `HashMap`.

**Q3: What is a "fail-fast" iterator?**
A: An iterator that immediately throws an error if it detects the underlying collection was changed unexpectedly while being looped through (see section 6.6).

## 6.10 Common Mistakes

- Removing items from a list using a normal for-each loop instead of an `Iterator` (causes a crash).
- Using `HashMap` when you actually need the items to stay in the order you inserted them (use `LinkedHashMap` instead).
- Forgetting to override `equals()` and `hashCode()` for custom objects used as keys in a `HashMap`/`HashSet` (see section 4.7).


---

# Part 7: Generics

> **📌 Definition:** Generics let classes, interfaces, and methods operate on a type parameter specified at compile time, giving type safety without manual casting.
>
> **Main points interviewers expect you to know:**
> - Compile-time type checking prevents `ClassCastException` at runtime.
> - `Box<T>` style generic classes; `T` is a placeholder decided at use-site.
> - Wildcards: `? extends T` (read-only, "Producer Extends") and `? super T` (write-only, "Consumer Super") — the PECS rule.
> - **Type erasure**: generic type info exists only at compile time; the JVM doesn't retain it at runtime (kept for backward compatibility).
> - Avoid mixing raw types and generic types.

## 7.1 What Are Generics? (Simple Explanation)

Before generics existed, collections like `ArrayList` could store ANY type of object mixed together, which was risky — you might accidentally put a `String` into a list meant for `Integer`s, and only discover the mistake when your program crashed at runtime.

**Generics let you specify, up front, exactly what type a class or method should work with.** Java then checks this at compile time, catching mistakes before your program even runs.

```java
List<String> names = new ArrayList<>();  // this list can ONLY hold Strings
names.add("Alice");      // fine
names.add(123);          // compile error! Java catches this immediately
```

You can also create your OWN generic classes:

```java
class Box<T> {              // T is a "placeholder" type, decided later
    private T item;
    public void set(T item) { this.item = item; }
    public T get() { return item; }
}

Box<String> stringBox = new Box<>();   // here, T becomes String
Box<Integer> intBox = new Box<>();     // here, T becomes Integer
```

## 7.2 Wildcards (`? extends` and `? super`) — A Bit Advanced

These let you write flexible methods that work with a *range* of related types.

```java
void printNumbers(List<? extends Number> list) { }  // accepts a list of Number OR any subtype (Integer, Double, etc.)
```

**Simple memory trick — PECS: "Producer Extends, Consumer Super":**
- Use `? extends T` when you're only **reading** values out (the list "produces" data for you).
- Use `? super T` when you're only **adding** values in (the list "consumes" data from you).

## 7.3 Interview Questions

**Q1: Why use generics instead of just using `Object` for everything?**
A: Generics give you compile-time type safety, catching mistakes early, and remove the need for manual, risky casting.

**Q2: What is type erasure?**
A: Generic type information only exists while you're writing/compiling code — at runtime, the JVM doesn't actually know the specific type was used (it's all "erased" down to a general type). This is mainly for backward compatibility with old Java code written before generics existed.

## 7.4 Common Mistakes

- Mixing generic and non-generic ("raw") types, which brings back the same type-safety risks generics were meant to prevent.

---

# Part 8: Multithreading & Concurrency

> **📌 Definition:** Multithreading is the ability to run multiple threads (independent paths of execution) concurrently within a single program, sharing the same process memory.
>
> **Main points interviewers expect you to know:**
> - Always call `.start()` (creates a new thread), never `.run()` (runs on the current thread).
> - **Race condition** — unsynchronized concurrent access/modification of shared data causes unpredictable results.
> - `synchronized` — only one thread executes the block/method at a time (prevents race conditions, has performance cost).
> - `volatile` — guarantees visibility of the latest value across threads, but NOT atomicity for compound operations like `count++`.
> - `wait()` releases the lock while waiting; `sleep()` keeps holding the lock.
> - Modern tools: `ExecutorService`, `Future`, `ConcurrentHashMap`, `AtomicInteger`.
> - **Virtual Threads (Java 21+)** — lightweight, JVM-managed threads for massive-scale I/O-bound concurrency.

## 8.1 What is a Thread? (Simple Explanation)

Normally, a program runs one instruction at a time, in order. A **thread** is like a separate "worker" that can run a piece of your program independently — and you can have MULTIPLE threads running at the same time, doing different things simultaneously. This is called **multithreading**.

**Why does this matter?** Imagine a music app — one thread plays the music, while another thread waits for you to tap buttons, while another downloads the next song. Without multithreading, the app would freeze completely while downloading.

```java
Runnable task = () -> System.out.println("Running in a separate thread!");
Thread thread = new Thread(task);
thread.start();   // starts a NEW thread that runs the task
```

> **Important beginner trap:** Always call `.start()`, not `.run()`. Calling `.run()` directly just executes the code normally, on your current thread — no actual new thread gets created.

## 8.2 The Problem Multithreading Creates: Race Conditions

If two threads try to read AND modify the same shared piece of data at the same time, things can go wrong unpredictably. This is called a **race condition**.

**Simple example of the problem:** Imagine two people trying to withdraw money from the same bank account at the exact same moment — without proper coordination, the bank might lose track of the correct balance.

**The fix: `synchronized`** — this keyword ensures only ONE thread can execute a piece of code at a time, locking out others until it's done.

```java
class Counter {
    private int count = 0;
    public synchronized void increment() {  // only one thread can run this at a time
        count++;
    }
}
```

## 8.3 `volatile` — A Lighter-Weight Tool

`volatile` ensures that when one thread updates a variable, all OTHER threads immediately see the new value (instead of possibly using an old, cached copy). However, unlike `synchronized`, it does NOT prevent race conditions for compound operations like `count++` (which is actually "read, then add, then write" — three separate steps that can still get mixed up between threads).

| | `synchronized` | `volatile` |
|---|---|---|
| Prevents race conditions | Yes | No (only for simple read/write, not for compound operations) |
| Ensures threads see the latest value | Yes | Yes |
| Performance cost | Higher | Lower |

## 8.4 Useful Modern Concurrency Tools

Rather than manually managing `Thread` objects, modern Java code usually uses higher-level tools from `java.util.concurrent`:

| Tool | What it's for, in plain words |
|---|---|
| `ExecutorService` | A reusable pool of worker threads — you submit tasks, and it manages running them efficiently, instead of you manually creating threads |
| `Future` | Represents a result that will be available LATER, once a background task finishes |
| `ConcurrentHashMap` | A version of HashMap that's safe to use from multiple threads at once, without needing manual `synchronized` blocks |
| `AtomicInteger` | A thread-safe counter — solves the `count++` problem mentioned above, without needing full `synchronized` locking |

```java
ExecutorService pool = Executors.newFixedThreadPool(4);  // a pool of 4 worker threads
Future<Integer> result = pool.submit(() -> 5 + 5);
System.out.println(result.get());  // waits for and prints the result: 10
pool.shutdown();
```

## 8.5 Virtual Threads (Java 21+) — A Big Modern Improvement

Traditional threads are somewhat "heavy" — creating thousands of them can use a lot of memory and slow down your computer. **Virtual threads** (introduced in Java 21) are extremely lightweight, JVM-managed threads — you can create MILLIONS of them without issues.

**Why does this matter?** They're perfect for programs that spend a lot of time waiting (like waiting for a network response), letting you write simple, easy-to-understand code that still scales to handle huge numbers of simultaneous tasks.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> System.out.println("Running on a lightweight virtual thread"));
}
```

## 8.6 Interview Questions

**Q1: What is a race condition, and how do you prevent it?**
A: When multiple threads access/modify shared data at the same time, causing unpredictable results. Prevent it using `synchronized`, locks, or thread-safe tools like `AtomicInteger`/`ConcurrentHashMap`.

**Q2: Difference between `wait()` and `sleep()`?**
A: `wait()` releases the lock it's holding while waiting (so other threads can proceed); `sleep()` keeps the lock the entire time it's pausing.

**Q3: What problem do virtual threads solve?**
A: They remove the heavy memory/performance cost of traditional threads, letting programs handle huge numbers of simultaneous, mostly-waiting tasks (like network requests) easily.

## 8.7 Common Mistakes

- Calling `.run()` instead of `.start()` (doesn't actually create a new thread).
- Assuming `volatile` alone makes `count++` safe — it doesn't; use `AtomicInteger` or `synchronized` instead.
- Forgetting that multiple threads modifying shared data without any coordination WILL eventually cause bugs, even if it seems to "work" most of the time during testing.


---

# Part 9: File Handling

> **📌 Definition:** File handling in Java is reading/writing data to files using I/O streams (byte/character streams) or the modern `java.nio.file` API.
>
> **Main points interviewers expect you to know:**
> - `FileReader`/`BufferedReader` (legacy, character streams) vs `Files.readAllLines()`/`Files.writeString()` (modern NIO, simpler).
> - Always use try-with-resources for streams/files to guarantee they're closed.
> - **Serialization** converts an object's state to bytes (`Serializable`); **deserialization** reverses it.
> - `transient` excludes a field from serialization (e.g., passwords).

## 9.1 Reading and Writing Files — Simple Explanation

Java lets you read data from files (like text files) and write data back to them, using "streams" — think of a stream like a pipe through which data flows, either into your program (reading) or out of it (writing).

```java
// Reading a text file, line by line
try (BufferedReader br = new BufferedReader(new FileReader("data.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}
```

**Modern, simpler way (using `java.nio.file`):**

```java
Path path = Path.of("data.txt");
List<String> lines = Files.readAllLines(path);   // reads the whole file into a list, in one line
Files.writeString(path, "Hello!");                // writes text to a file, in one line
```

## 9.2 Serialization — Saving Objects to Disk

**Serialization** means converting an object's current state into a stream of bytes, so it can be saved to a file or sent over a network. **Deserialization** is the reverse — rebuilding the object from those bytes later.

```java
class User implements Serializable {
    String name;
    transient String password;   // "transient" means: skip this field during serialization
}
```

The `transient` keyword is useful for excluding sensitive data (like passwords) from being saved.

## 9.3 Interview Questions

**Q1: What does `transient` do?**
A: It tells Java to skip that specific field when saving (serializing) an object — useful for sensitive or temporary data.

**Q2: Why use try-with-resources for files?**
A: It automatically closes the file/stream for you, even if an error happens, preventing resource leaks (where files stay "locked" or open unnecessarily).

**Q3: What is the difference between byte streams and character streams?**
A: Byte streams (`InputStream`/`OutputStream`) handle raw binary data (e.g., images); character streams (`Reader`/`Writer`) handle text and automatically deal with character encoding.

**Q4: What happens if a class doesn't implement `Serializable` but you try to serialize it?**
A: Java throws a `NotSerializableException` at runtime.

## 9.4 Common Mistakes

- Forgetting to close streams (or not using try-with-resources), causing resource leaks.
- Not marking sensitive fields as `transient` before serializing an object.

---

# Part 10: Interfaces, Abstract Classes, Inner Classes & Enums

> **📌 Definition:** An interface is a contract of method signatures a class agrees to implement; an enum is a fixed, named set of constants; inner classes are classes nested inside another class.
>
> **Main points interviewers expect you to know:**
> - Interfaces can have `default` (with body, optional override) and `static` methods since Java 8 — added for backward-compatible API evolution.
> - Abstract class: single inheritance, can hold shared state/code. Interface: multiple "implements" allowed, defines pure capability.
> - 4 kinds of inner classes: member, static nested, local, anonymous (often replaced by lambdas).
> - Enums are type-safe constants and can have fields/constructors/methods of their own.

## 10.1 Interfaces — A Contract, Not an Implementation

An **interface** defines WHAT a class must be able to do, without saying HOW it does it. Think of it like a job description — it lists the required skills, but not how each person performs them.

```java
interface Vehicle {
    void drive();   // any class implementing Vehicle MUST provide its own drive() method
}

class Car implements Vehicle {
    public void drive() { System.out.println("Driving a car"); }
}
```

**Since Java 8, interfaces can also have:**
- **`default` methods** — methods WITH a body, that implementing classes can use as-is or override.
- **`static` methods** — utility methods that belong to the interface itself.

```java
interface Vehicle {
    void drive();
    default void honk() { System.out.println("Beep!"); }  // has a body — optional to override
}
```

**Why were default methods added?** So that library creators could add new functionality to existing interfaces, without breaking all the classes that already implement them (which would otherwise be forced to suddenly implement the new method too).

## 10.2 Abstract Classes vs Interfaces — A Simple Comparison

| | Abstract Class | Interface |
|---|---|---|
| Can contain fully-working methods? | Yes | Yes (with `default`, since Java 8) |
| Can contain unfinished methods? | Yes | Yes |
| How many can a class inherit from? | Only 1 | As many as needed |
| Best used when | Subclasses share a lot of common code/state | You just want to define a capability (a "can-do" contract) |

## 10.3 Inner Classes — Classes Inside Classes

Sometimes a class only makes sense within the context of another class. Java lets you nest classes inside each other.

```java
class Outer {
    class Inner {   // tied to a specific instance of Outer
        void show() { System.out.println("Inner class"); }
    }
}
```

There are 4 types: member inner classes, static nested classes, local inner classes (defined inside a method), and anonymous inner classes (a one-time, unnamed class — often replaced by lambdas in modern code).

## 10.4 Enums — A Fixed Set of Named Constants

An **enum** represents a fixed list of possible values — like the days of the week, or the suits in a deck of cards.

```java
enum Day { MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY }

Day today = Day.MONDAY;
```

Enums can even have their own fields and methods, just like a regular class:

```java
enum Planet {
    MERCURY(3.3e23), EARTH(5.9e24);
    final double mass;
    Planet(double mass) { this.mass = mass; }
}
```

## 10.5 Interview Questions

**Q1: Why were `default` methods added to interfaces?**
A: To let library designers safely add new methods to existing interfaces without breaking classes that already implement them — see section 10.1.

**Q2: Can an enum have a constructor?**
A: Yes, but it's always private/internal — each enum constant is only ever created once, automatically, when the program starts.

## 10.6 Common Mistakes

- Trying to instantiate a (non-static) inner class without first having an instance of its outer class.
- Forgetting that an enum constructor can't be called manually like a normal class constructor.


---

# Part 11: Annotations & Reflection

> **📌 Definition:** Annotations are metadata tags attached to code that instruct the compiler or frameworks (without changing runtime logic directly); reflection lets a program inspect/modify its own classes, methods, and fields at runtime.
>
> **Main points interviewers expect you to know:**
> - Built-in annotations: `@Override`, `@Deprecated`, `@SuppressWarnings`, `@FunctionalInterface`.
> - Frameworks (Spring, JUnit) rely heavily on annotations + reflection for dependency injection and test discovery.
> - Reflection can access private members, but is slower and can break encapsulation — used carefully, mainly in frameworks.

## 11.1 Annotations — Notes for the Compiler/Tools

An **annotation** is like a sticky note attached to your code — it doesn't directly change how the code runs, but it gives instructions/information to the compiler or other tools.

```java
@Override          // tells the compiler "I intend to override a parent method" — catches typos
void sound() { }

@Deprecated         // marks this as outdated, discouraging others from using it
void oldMethod() { }
```

**Why are annotations useful?** Frameworks like Spring or testing tools like JUnit heavily rely on annotations (e.g., `@Test`, `@Autowired`) to know what to do with your code, without you needing to write a lot of manual setup/configuration.

## 11.2 Reflection — Inspecting Code at Runtime

**Reflection** lets your program examine and even modify classes, methods, and fields WHILE it's running — even private ones it normally wouldn't have access to.

```java
Class<?> clazz = Person.class;
Method[] methods = clazz.getDeclaredMethods();   // lists all methods, even private ones
```

**Why does this matter?** It's how frameworks like Spring can automatically figure out and "wire together" your classes, and how testing tools can automatically find and run your `@Test` methods, without you manually registering anything.

**Downside:** Reflection is slower than normal code, and can break the protections that `private` access is meant to provide — so it's used carefully, mostly inside frameworks/libraries rather than everyday application code.

## 11.3 Interview Questions

**Q1: What's a real-world use case for reflection?**
A: Frameworks like Spring use it to automatically create and connect objects (dependency injection), and testing tools like JUnit use it to find and run methods marked with `@Test`.

**Q2: What's the purpose of `@Override`?**
A: It tells the compiler you intend to override a parent method, so it can catch typos (e.g., wrong method signature) as a compile error instead of silently creating a new, unrelated method.

**Q3: What is a meta-annotation?**
A: An annotation that applies to other annotations, like `@Retention` (controls how long an annotation is kept — source, class, or runtime) and `@Target` (restricts where an annotation can be applied).

## 11.4 Common Mistakes

- Overusing reflection in everyday application code instead of normal method calls, hurting performance and readability.
- Forgetting that annotations alone do nothing — they need a compiler check, framework, or reflection-based processor to actually act on them.

---

# Part 12: Design Patterns

> **📌 Definition:** Design patterns are reusable, proven solutions to common software design problems — a shared vocabulary for structuring code, not ready-made code itself.
>
> **Main points interviewers expect you to know:**
> - **Singleton** — exactly one instance, via a private constructor + static accessor.
> - **Factory** — centralizes object creation logic, hides which exact subclass gets instantiated.
> - **Builder** — constructs complex objects step-by-step, useful when many fields are optional.
> - **Observer** — notifies a list of dependent "listeners" automatically when state changes (basis of event-driven systems).

**Simple idea:** Design patterns are well-known, proven solutions to common coding problems — like a recipe you can follow, rather than a piece of ready-made code.

## 12.1 Singleton — "Only One Instance, Ever"

**Use case:** Sometimes you want to guarantee only ONE instance of a class exists in your entire program — like a single configuration manager or a single database connection pool.

```java
class Singleton {
    private static Singleton instance;
    private Singleton() { }  // private constructor — nobody outside can create one directly

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();  // created only the FIRST time it's needed
        }
        return instance;
    }
}
```

## 12.2 Factory — "Let a Helper Decide What to Create"

**Use case:** Instead of the calling code deciding exactly which class to instantiate, a "factory" method does that decision-making for you, based on some input.

```java
class ShapeFactory {
    static Shape createShape(String type) {
        if (type.equals("circle")) return new Circle();
        if (type.equals("square")) return new Square();
        return null;
    }
}
```

## 12.3 Builder — "Build Complex Objects Step by Step"

**Use case:** When a class has MANY optional fields, having a constructor with 10 parameters becomes confusing. The Builder pattern lets you set only what you need, one piece at a time.

```java
Pizza pizza = new Pizza.Builder()
    .size("Large")
    .topping("Cheese")
    .topping("Mushroom")
    .build();
```

## 12.4 Observer — "Notify Everyone When Something Changes"

**Use case:** When one object changes, automatically notify a list of "listeners" who care about that change. This is the foundation of how button-click listeners and event systems work.

## 12.5 Interview Questions

**Q1: Why use a private constructor in Singleton?**
A: To prevent any code outside the class from creating new instances directly — the only way to get an instance is through the controlled `getInstance()` method.

**Q2: Difference between Factory and Builder patterns?**
A: Factory creates a complete object in one single step, hiding which exact class gets used. Builder constructs a complex object gradually, step-by-step, which is helpful when there are many optional settings.

---

# Part 13: JVM, Memory & Garbage Collection

> **📌 Definition:** The JVM is the runtime engine that loads, verifies, and executes Java bytecode; Garbage Collection is its automatic process for reclaiming memory occupied by unreachable objects.
>
> **Main points interviewers expect you to know:**
> - JVM = Class Loader + Runtime Data Areas (Stack, Heap, Metaspace) + Execution Engine (Interpreter, JIT compiler, GC).
> - An object becomes eligible for GC once nothing references it anymore.
> - Generational GC: Young Generation (frequent, fast Minor GC) vs Old Generation (less frequent, slower Major/Full GC).
> - `System.gc()` only *requests* collection — never guaranteed.
> - `OutOfMemoryError` (heap exhausted) vs `StackOverflowError` (uncontrolled recursion).

## 13.1 Where Does Java Store Things in Memory?

| Area | What it stores | Simple explanation |
|---|---|---|
| **Stack** | Local variables, method calls | Like a stack of plates — grows/shrinks as methods are called/finished |
| **Heap** | All objects (anything made with `new`) | A big shared space where objects "live" until no longer needed |
| **Metaspace** | Information ABOUT your classes themselves | Replaced an older area called "PermGen" in Java 8 |

## 13.2 Garbage Collection — Automatic Memory Cleanup

**Simple idea:** In languages like C, programmers must manually free memory they're done using — forgetting to do this causes memory leaks. Java automates this entirely with the **Garbage Collector (GC)**.

**How it decides what to clean up:** An object becomes "garbage" (eligible for cleanup) once NOTHING in your program can reach/reference it anymore.

```java
Person p = new Person();
p = null;   // the original Person object can no longer be reached by anything →
            // it becomes eligible for garbage collection
```

**Why split memory into "generations"?** Java observed that most objects are short-lived (created and discarded quickly), while a few live a long time. So the heap is split:
- **Young Generation** — where new objects are born; cleaned frequently and quickly ("Minor GC").
- **Old Generation** — where long-surviving objects eventually get moved; cleaned less often, but takes longer ("Major/Full GC").

## 13.3 Interview Questions

**Q1: Can you force garbage collection to happen?**
A: You can *request* it with `System.gc()`, but the JVM is free to ignore your request — it's never guaranteed to run immediately.

**Q2: What's the difference between `OutOfMemoryError` and `StackOverflowError`?**
A: `OutOfMemoryError` happens when the heap runs out of space for new objects. `StackOverflowError` happens when a method calls itself too many times without stopping (uncontrolled recursion), filling up the stack.

## 13.4 Common Mistakes

- Believing `System.gc()` immediately and definitely frees memory — it's only a suggestion, not a command.
- Accidentally keeping references to objects you no longer need (e.g., in a static list), which prevents the garbage collector from ever cleaning them up — this is called a memory leak, even in a "managed memory" language like Java.


---

# Part 14: Modern Java Features (Java 8 → Java 25)

> **📌 Definition:** "Modern Java" refers to the major language and API improvements introduced from Java 8 onward — lambdas, streams, records, pattern matching, virtual threads, and structured concurrency — that make code shorter, safer, and more scalable.
>
> **Main points interviewers expect you to know:**
> - Java 8: Lambdas, Stream API, `Optional`, new Date/Time API, functional interfaces.
> - `var` (Java 10) is type inference, not dynamic typing — type is fixed at compile time.
> - Records (Java 16) auto-generate constructor, accessors, `equals()`, `hashCode()`, `toString()`.
> - Pattern matching for `instanceof`/`switch` removes manual casting.
> - Sealed classes (Java 17) restrict which classes can extend/implement a type, enabling exhaustive `switch` checks.
> - Virtual Threads (Java 21) — lightweight JVM-managed threads for massive I/O-bound concurrency.
> - Java 25 (latest LTS): stable Structured Concurrency, simplified `main` method.

This is the part interviewers love to ask about — it shows you keep your knowledge up to date. Java releases a new version every 6 months, but only some versions get **Long-Term Support (LTS)**: Java **8, 11, 17, 21, and 25**. As of mid-2026, most companies use Java 17 or 21, with newer teams adopting Java 25 (the latest LTS, released September 2025).

## 14.1 Java 8 — The Most Important Update Ever

### Lambda Expressions — "A Quick Way to Write a Function"

Before Java 8, if you wanted to pass behavior (like "what to do when a button is clicked") as a parameter, you had to write a whole extra class. Lambdas let you write this inline, in one short line.

```java
// Old way:
Runnable r = new Runnable() {
    public void run() { System.out.println("Hello"); }
};

// New way, with a lambda:
Runnable r = () -> System.out.println("Hello");
```

A lambda can only be used where Java expects a **functional interface** — an interface with exactly ONE method that needs implementing (like `Runnable`'s single `run()` method).

### The Stream API — "Process Collections Like a Pipeline"

Instead of writing manual loops to filter, transform, and collect data, Streams let you describe WHAT you want, in a clean, readable chain.

```java
List<String> names = List.of("Alice", "Bob", "Charlie");

List<String> result = names.stream()
    .filter(n -> n.length() > 3)     // keep only names longer than 3 letters
    .map(String::toUpperCase)         // convert each to uppercase
    .sorted()                         // sort alphabetically
    .collect(Collectors.toList());    // gather the results into a list
```

Read this top to bottom like a sentence: "take the names, keep ones longer than 3 letters, uppercase them, sort them, and collect into a list."

### Optional — "A Safer Way to Say 'Maybe No Value'"

`Optional` is a small wrapper that explicitly says "this might or might not contain a value," forcing you to handle the missing case instead of accidentally getting a `NullPointerException`.

```java
Optional<String> name = Optional.ofNullable(getName());
String result = name.orElse("Unknown");   // use "Unknown" if no name was found
```

### Method References — "An Even Shorter Lambda"

If your lambda just calls an already-existing method, you can shorten it further:

```java
names.forEach(System.out::println);   // same as: names.forEach(n -> System.out.println(n));
```

### The New Date and Time API

Java's old `Date`/`Calendar` classes were confusing and error-prone (and surprisingly, mutable). Java 8 introduced clean, modern replacements:

```java
LocalDate today = LocalDate.now();
LocalDate birthday = LocalDate.of(1995, 6, 15);
```

## 14.2 Java 9–11 — Smaller, Practical Improvements

- **`var` keyword (Java 10):** lets you skip writing the type explicitly when it's obvious from context.
```java
var list = new ArrayList<String>();   // Java figures out it's an ArrayList<String> on its own
```
  Important: Java is still strongly typed — `var` just saves you typing, it doesn't make Java "dynamically typed." Once assigned, you can't change the variable's type later.
- **Convenient collection creation (Java 9):** `List.of("a", "b", "c")` creates a small, unchangeable list in one line.
- **More String helper methods (Java 11):** `isBlank()`, `strip()`, `repeat(n)` — small but handy additions.

## 14.3 Records (Java 16) — "Less Boilerplate for Simple Data Classes"

If you've ever written a simple class JUST to hold a few values (with a constructor, getters, `equals()`, `hashCode()`, `toString()`), you know how repetitive it gets. A `record` does all of this automatically, in one line.

```java
record Point(int x, int y) { }

Point p = new Point(3, 4);
System.out.println(p.x());          // 3 — accessor method, automatically generated
System.out.println(p);              // Point[x=3, y=4] — toString() also auto-generated
```

## 14.4 Pattern Matching (Java 16–21) — "Smarter Type Checking"

Normally, checking and casting a type took two steps:

```java
// Old way:
if (obj instanceof String) {
    String s = (String) obj;   // manual casting needed
    System.out.println(s.length());
}

// New way (pattern matching, Java 16+):
if (obj instanceof String s) {   // automatically casts "obj" into "s" if the check passes
    System.out.println(s.length());
}
```

This was extended to `switch` in Java 21:

```java
String describe(Object obj) {
    return switch (obj) {
        case Integer i -> "An integer: " + i;
        case String s  -> "A string: " + s;
        default        -> "Something else";
    };
}
```

## 14.5 Sealed Classes (Java 17) — "A Closed, Controlled Set of Subclasses"

Sometimes you want inheritance, but you want to STRICTLY control which classes are allowed to extend a given class — nothing else.

```java
sealed interface Shape permits Circle, Square { }
record Circle(double radius) implements Shape { }
record Square(double side) implements Shape { }
```

**Why this is useful:** Because Java knows EXACTLY which subclasses are possible, it can check at compile time that you've handled every single case in a `switch` — no risk of accidentally forgetting one.

## 14.6 Virtual Threads (Java 21) — Already Explained in Part 8.5

A massive concurrency improvement — extremely lightweight threads that let you handle huge numbers of simultaneous tasks (especially network/I/O work) with simple, readable code.

## 14.7 Java 25 (LTS, September 2025) — The Newest Long-Term Version

- **Structured Concurrency (now stable):** lets you treat a GROUP of related background tasks as one single unit — if one fails, all the others are automatically cancelled too, instead of leaving "orphaned" tasks running in the background.
- **Simplified main method:** for small/simple programs, you no longer need the full ceremony of `public class X { public static void main(String[] args) { ... } }` — Java 25 allows simpler entry points for beginners and quick scripts.

```java
void main() {
    println("Hello, Java 25!");
}
```

- **Value Objects (a preview/experimental feature):** part of an ongoing effort (Project Valhalla) to make simple, identity-free objects more memory-efficient under the hood.

## 14.8 Quick Summary Table

| Version | Headline Feature(s) |
|---|---|
| Java 8 (LTS) | Lambdas, Streams, Optional, new Date/Time API |
| Java 9 | Modules, `List.of()`/`Set.of()`/`Map.of()` |
| Java 10 | `var` keyword |
| Java 11 (LTS) | New `HttpClient`, more String methods |
| Java 14 | Switch expressions (`->` syntax) |
| Java 16 | Records, Pattern Matching for `instanceof` |
| Java 17 (LTS) | Sealed classes |
| Java 21 (LTS) | Virtual Threads, Record Patterns, Pattern Matching for `switch` |
| Java 25 (LTS, current latest) | Structured Concurrency (stable), simplified `main` method |

## 14.9 Interview Questions

**Q1: What problem do Streams solve, compared to regular loops?**
A: They let you describe WHAT you want done (filter, transform, collect), in a clean, readable chain, instead of writing manual step-by-step loops — and they're easy to run in parallel if needed.

**Q2: Why use `Optional` instead of just returning `null`?**
A: It forces the calling code to explicitly think about and handle the "no value found" case, reducing accidental `NullPointerException`s.

**Q3: What problem do Records solve?**
A: They remove repetitive boilerplate code for simple, immutable data-holding classes — no need to manually write constructors, getters, `equals()`, `hashCode()`, and `toString()`.

**Q4: What are Virtual Threads, and why are they a big deal?**
A: Extremely lightweight, JVM-managed threads (introduced in Java 21) that let you handle huge numbers of waiting/I/O-bound tasks cheaply, without the heavy cost of traditional threads.

## 14.10 Common Mistakes

- Using `parallelStream()` for small lists or for tasks that mostly wait on network/disk — the overhead isn't worth it; it's best for large, CPU-heavy work.
- Forgetting `var` is still strongly typed — you cannot reassign a `var` variable to a completely different type later.
- Using `Optional` for fields or method parameters — it's designed mainly as a RETURN type, to clearly signal "this might be empty" to the caller.


---

# Part 15: Coding Patterns for Interviews

Most coding interview questions aren't actually unique — they're variations of a small set of common "patterns." Recognizing which pattern applies is often the hardest part; once you do, the solution becomes much easier.

| Pattern | When to use it | Example problems |
|---|---|---|
| **Two Pointers** | Working with a sorted array, looking for pairs | Finding two numbers that add up to a target |
| **Sliding Window** | Looking at a "moving section" of an array/string | Longest substring without repeating characters |
| **Fast & Slow Pointers** | Detecting cycles in a linked list | Detect if a linked list loops back on itself |
| **Binary Search** | Searching efficiently in sorted data | Finding an item, or the "smallest valid value" |
| **BFS / DFS** | Exploring trees, graphs, or grids | Counting connected "islands" in a grid |
| **Backtracking** | Generating all possible combinations | All subsets, all permutations |
| **Dynamic Programming** | A problem breaks into smaller, repeating subproblems | Fibonacci, knapsack-style problems |
| **Heap (Priority Queue)** | Need the "top K" or smallest/largest items, repeatedly | Find the Kth largest number |

**Example: Sliding Window pattern in action**

```java
// Find the length of the longest substring with no repeating characters
int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> seen = new HashMap<>();
    int maxLen = 0, start = 0;
    for (int end = 0; end < s.length(); end++) {
        char c = s.charAt(end);
        if (seen.containsKey(c)) {
            start = Math.max(start, seen.get(c) + 1);  // shrink the window if we see a repeat
        }
        seen.put(c, end);
        maxLen = Math.max(maxLen, end - start + 1);   // expand the window and track the max
    }
    return maxLen;
}
```

---

# Part 16: Top Interview Questions (Quick-Fire List)

**Core Java**
1. What are Java's 8 primitive types? *(see 1.5)*
2. Why is Java platform-independent? *(bytecode + JVM, see 1.2)*
3. Difference between `==` and `.equals()`? *(memory address vs content)*

**OOP**
4. What is dynamic method dispatch? *(see 4.4)*
5. Difference between abstract class and interface? *(see 4.9)*
6. Why must `equals()` and `hashCode()` be overridden together? *(see 4.7)*

**Strings & Collections**
7. Why is String immutable? *(see 2.2)*
8. How does HashMap work internally? *(see 6.5)*
9. ArrayList vs LinkedList — when to use each? *(see 6.2)*

**Exceptions**
10. Checked vs unchecked exceptions? *(see 5.2)*
11. Difference between `throw` and `throws`? *(see 5.5)*

**Multithreading**
12. What is a race condition? *(see 8.2)*
13. What are Virtual Threads, and why do they matter? *(see 8.5)*

**Modern Java**
14. What is a functional interface? *(an interface with exactly one method to implement)*
15. What problem do Records solve? *(see 14.3)*
16. What's the difference between an old-style `switch` statement and a modern `switch` expression? *(the new version uses `->`, doesn't fall through, and can directly return a value)*

**JVM & Memory**
17. Stack vs Heap memory? *(see 1.6)*
18. What is garbage collection, and how does Java decide what to clean up? *(see 13.2)*

---

# Part 17: Common Mistakes (All Topics, Consolidated)

- Using `==` instead of `.equals()` to compare object/String content.
- Overriding `equals()` without also overriding `hashCode()` (or vice versa).
- Building Strings with `+` inside a loop, instead of using `StringBuilder`.
- Modifying a list/map while looping through it with a regular for-each loop.
- Catching the generic `Exception` type instead of being specific about which errors you expect.
- Calling `.run()` instead of `.start()` on a `Thread` (doesn't create a real new thread).
- Believing `volatile` alone makes operations like `count++` thread-safe (it doesn't).
- Thinking Java passes objects "by reference" — it always passes the reference itself "by value."
- Forgetting local variables need to be manually given a value before use.
- Reaching for `parallelStream()` on small or I/O-heavy tasks where it actually slows things down.

---

# Part 18: Cheat Sheets & Quick Reference

## Collections Speed Reference

| Collection | Add | Remove | Search | Read by index |
|---|:---:|:---:|:---:|:---:|
| `ArrayList` | Fast | Slow (middle) | Slow | Fast |
| `LinkedList` | Fast | Fast (ends) | Slow | Slow |
| `HashMap` / `HashSet` | Fast | Fast | Fast | — |
| `TreeMap` / `TreeSet` | Medium | Medium | Medium | — |

## Quick Rules to Remember

1. Local variables = no automatic default value. Instance/static fields = automatic default values.
2. String literals share memory via the String Pool; `new String()` always creates a separate copy.
3. `==` compares memory addresses (for objects); `.equals()` compares actual content.
4. Checked exceptions must be handled/declared; unchecked ones (RuntimeException) don't have to be.
5. `sleep()` keeps its lock while waiting; `wait()` releases it.
6. Always call `.start()`, never `.run()`, to actually create a new thread.

---

# Part 19: Final Revision Plan & Glossary

## If You Have 1 Day Before the Interview
- Hours 1–2: Java basics, Stack vs Heap, Strings & the String Pool.
- Hours 3–4: OOP pillars, `equals()`/`hashCode()`, constructors.
- Hours 5–6: Collections (especially how HashMap works).
- Hours 7–8: Multithreading basics, Modern Java (Streams, Lambdas).
- Hour 9+: Re-read Part 17 (Common Mistakes) and Part 16 (Top Interview Questions).

## If You Have 3 Days
- Day 1: Fundamentals, Strings, Arrays, OOP, Exceptions.
- Day 2: Collections, Generics, Multithreading.
- Day 3: Modern Java (Part 14), Design Patterns, Coding Patterns (Part 15).

## Glossary (Simple Definitions)

- **Bytecode** — the "middle" format Java code is compiled into, which the JVM can run on any computer.
- **JVM** — the program that actually runs your compiled Java code.
- **Dynamic Method Dispatch** — Java deciding, at runtime, which version of an overridden method to actually run.
- **Functional Interface** — an interface with exactly one method that needs implementing (used for lambdas).
- **Garbage Collection** — Java's automatic system for cleaning up memory you no longer need.
- **Immutable** — something that can't be changed after it's created (like a String).
- **Race Condition** — a bug that happens when multiple threads access shared data at the same time, unsafely.
- **Record** — a quick way to define a simple, immutable data-holding class (Java 16+).
- **Sealed Class** — a class that only allows a specific, predefined list of subclasses.
- **Virtual Thread** — an extremely lightweight, JVM-managed thread (Java 21+), great for handling many waiting/I-O-bound tasks at once.

---

*This handbook is written to be simple, clear, and beginner-friendly — covering everything you need for Java placement interviews, updated through Java 25 LTS.*
