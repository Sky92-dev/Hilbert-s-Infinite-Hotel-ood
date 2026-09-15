# Hilbert's Infinite Hotel

An implementation of **Hilbert's Infinite Hotel** designed to manage an unlimited number of guests and dynamically assign unique rooms while following the rules of the problem.

The main focus of this project is **correctness, execution speed, and memory efficiency** when processing a large number of guests.

## 📌 Main Problem

The system must handle the following rules:

1. An unlimited number of guests can arrive through an unlimited number of transportation channels.
2. Every guest must have a unique room.
3. Existing guests cannot simply remain in their current rooms while new guests are assigned afterward. When new guests arrive, the existing guests must be relocated.
4. When new guests arrive, **all existing guests must receive new room numbers**, and their status changes to existing guests.
5. Rooms can be removed.
6. New rooms can be added.
7. Guest and room information can be exported to Excel.
8. The primary goals are **speed, memory efficiency, and correctness according to the problem's rules**.

## 💡 Solution

### 1. Guest Input

Guests can arrive through multiple transportation channels.

The input uses **Walk / W as the final channel** to indicate the number of arriving guests.

For example:

```text
Bus 1 / Train 2 / W 100
```

means:

* Bus 1
* Train 2
* 100 walking guests

Another example:

```text
Bus 1 / Train 2 / W 100
W 40
Bus 2 / Train 1 / W 20
```

represents multiple groups of guests arriving through different channels.

The input format allows the system to support a variable number of transportation channels.

---

## 2. Room Number Generation

Each guest's transportation information is converted into a unique numerical representation that is used to generate a room number.

The system uses **prime numbers as positional identifiers** for each transportation channel.

Conceptually:

```text
Transportation Information
        ↓
Convert each channel to a value
        ↓
Map each channel to a prime number
        ↓
Calculate room number
```

The room number is generated using a prime-based mathematical representation:

```text
room_number =
(v₁ + 1)^p₁ ×
(v₂ + 1)^p₂ ×
(v₃ + 1)^p₃ × ...
```

where:

* `v` represents the value associated with each transportation channel.
* `p` represents a unique prime number assigned to that channel.

For example, a simplified input such as:

```text
Train 1 / Bus 2 / Walk 100
```

can be represented using different prime exponents for each channel.

This approach provides a deterministic way to generate a room number from the guest's input information.

---

## 3. Handling Duplicate Room Numbers

Although the generated room number is based on the guest's information, the system must still ensure that no two guests occupy the same room.

Before assigning a room, the system checks whether the generated room number already exists.

```python
room_number = self.find_room_number(guest_info)

if self.Hash_table.get(room_number) is not None:
    i = 0
    new_room_number = room_number

    while self.Hash_table.get(new_room_number) is not None:
        i += 1
        new_room_number = room_number + i**2

    room_number = new_room_number
```

If the room is already occupied, the system generates another available room number.

The final room number is then stored in the data structures used by the system.

---

## 4. Data Structures

Two main data structures are used to manage the room information.

### Dictionary / Hash Table

The Dictionary is used for **fast room lookup**.

```text
Room Number
     ↓
Hash Table
     ↓
Guest / Room Information
```

This allows the system to quickly determine whether a room number already exists without searching through every room.

### Treap

A **Treap** is used to maintain the room numbers in sorted order.

```text
              Treap
                │
        ┌───────┴───────┐
        ↓               ↓
    Smaller          Larger
   Room Number      Room Number
```

The Treap provides an efficient way to maintain and process ordered room information.

### Why Use Both?

The two structures have different purposes:

| Data Structure          | Main Purpose                     |
| ----------------------- | -------------------------------- |
| Dictionary / Hash Table | Fast lookup                      |
| Treap                   | Maintain sorted room information |

Using both allows the system to avoid relying on a single data structure for every operation.

---

##  Guest Management Flow

When a new guest group arrives:

```text
New Guest Input
      ↓
Parse Transportation Information
      ↓
Generate Room Number
      ↓
Check Dictionary
      ↓
┌─────┴─────┐
│           │
Exists     Available
│           │
↓           ↓
Generate   Assign
New Room   Room
│           │
└─────┬─────┘
      ↓
Insert into Dictionary
      ↓
Insert into Treap
```

The assigned room is stored in both the **Hash Table** and **Treap**.

---

##  Performance Focus

Because the problem can involve a very large number of guests, performance is one of the main considerations of this project.

The implementation focuses on:

* **Execution Time**
* **Memory Usage**
* **Correctness**
* **Scalability**

The system is designed to process large datasets while maintaining efficient lookup and ordered data management.

##  Excel Export

The system also supports exporting guest and room information to **Excel**, allowing the generated data to be inspected and analyzed outside the application.

## 🎯 Objectives

* Implement Hilbert's Infinite Hotel problem
* Handle an unlimited number of guest groups and transportation channels
* Guarantee unique room assignments
* Support dynamic room insertion and deletion
* Apply appropriate data structures to improve performance
* Analyze execution time and memory consumption
* Maintain correctness under the rules of the problem
* Export results for further analysis

##  Technologies

* **Python**
* **Data Structures & Algorithms**
* **Dictionary / Hash Table**
* **Treap**
* **Excel Export**

##  Key Concepts

This project demonstrates:

* Hash Tables
* Treap
* Prime Number Representation
* Searching
* Sorting
* Dynamic Data Management
* Algorithm Complexity
* Memory Optimization
* Performance Analysis


Computer Engineering
King Mongkut's Institute of Technology Ladkrabang (KMITL)
