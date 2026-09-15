import os, psutil
import pandas as pd
import time
import random
"พิมพ์ที่ pip install pandas openpyxl terminal ก่อน"


class HeapTree:
    class Node:
        __slots__ = ('data', 'priority', 'left', 'right')
        def __init__(self, data):
            self.data = data
            self.priority = random.random()
            self.left = None
            self.right = None

        def __str__(self):
            return f"{self.data}({self.priority:.3f})"

    def __init__(self):
        self.root = None

    # ----------------------------
    # add() / insert
    # ----------------------------
    def add(self, root, data):
        self.root = self._insert(root, data)
        return self.root

    def _insert(self, root, data):
        if root is None:
            return self.Node(data)
        if data < root.data:
            root.left = self._insert(root.left, data)
            if root.left.priority > root.priority:
                root = self._rotateRight(root)
        elif data > root.data:
            root.right = self._insert(root.right, data)
            if root.right.priority > root.priority:
                root = self._rotateLeft(root)
        return root

    # ----------------------------
    # delete()
    # ----------------------------
    def delete(self, data):
        self.root, deleted = self._delete(self.root, data)
        return deleted

    def _delete(self, root, data):
        if root is None:
            return None, False

        deleted = False
        if data < root.data:
            root.left, deleted = self._delete(root.left, data)
        elif data > root.data:
            root.right, deleted = self._delete(root.right, data)
        else:
            deleted = True
            # หมุนลงไปจนกลายเป็นใบ แล้วลบทิ้ง
            if root.left is None and root.right is None:
                return None, True
            elif root.left is None:
                root = self._rotateLeft(root)
                root.left, _ = self._delete(root.left, data)
            elif root.right is None:
                root = self._rotateRight(root)
                root.right, _ = self._delete(root.right, data)
            else:
                # หมุนฝั่งที่ priority สูงกว่า
                if root.left.priority > root.right.priority:
                    root = self._rotateRight(root)
                    root.right, _ = self._delete(root.right, data)
                else:
                    root = self._rotateLeft(root)
                    root.left, _ = self._delete(root.left, data)
        return root, deleted

    # ----------------------------
    # Rotation helpers
    # ----------------------------
    def _rotateRight(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotateLeft(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    # ----------------------------
    # InOrder traversal
    # ----------------------------
    def InOrder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node)
            self._inorder(node.right, result)

class Hash_Table:
    def __init__(self):
        self.table = {}

    # --- insert ---
    def insert(self, key, value):
        self.table[key] = value
        return True

    # --- get ---
    def get(self, key):
        return self.table.get(key)

    # --- delete ---
    def delete(self, key):
        return self.table.pop(key, None) is not None

    # --- utility ---
    def __len__(self):
        return len(self.table)

    def __str__(self):
        return str(self.table)


class Hotel:
    def __init__(self):
        self.HeapTree = HeapTree()
        self.Hash_table = Hash_Table()
        self.prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    def manage_current_guest(self):
        temp_hash = Hash_Table()   # ✅ ไม่ใช้ capacity แล้ว
        count = [0]

        self._manage_current_guest(self.HeapTree.root, temp_hash, count)
        self.Hash_table = temp_hash

        print("-----------------------------------")
        
    def _manage_current_guest(self, root, temp_hash, count):
        if root:
            self._manage_current_guest(root.left, temp_hash, count)
            
            new_room_number = (count[0]+1)**2
            root.data = new_room_number
            temp_hash.insert(new_room_number, 0)  
            count[0] += 1
            
            self._manage_current_guest(root.right, temp_hash, count)
    
    def find_room_number(self, guest_info):
        room_number = 1
        i = 0
        
        for v in guest_info:
            if i == 1 and v == 0:
                v = 1
            if i >= len(self.prime_list):
                self.prime_list.append(self._next_prime(self.prime_list[i]))

            room_number *= (v + 1) ** self.prime_list[i]
            
            i += 1
            
        return room_number
    def _next_prime(n):
        # คืนค่า prime number ที่มากกว่าหรือเท่ากับ n
        def is_prime(x):
            if x < 2: return False
            for i in range(2, int(x**0.5)+1):
                if x % i == 0: return False
            return True
        while not is_prime(n):
            n += 1
        return n
    
    def add_new_guest(self,root,guest_info):
        room_number = self.find_room_number(guest_info)

        if self.Hash_table.get(room_number) is not None:
            i = 0
            new_room_number = room_number
            
            while self.Hash_table.get(new_room_number) is not None:
                i += 1
                new_room_number = room_number + i**2
            room_number = new_room_number
        self.Hash_table.insert(room_number, 1)
        new_root = self.HeapTree.add(root,room_number)

        return new_root

    def manage_new_guest(self, new_guest_list):
        self.manage_current_guest()  # จัดแขกเก่าเรียบร้อย
        root = self.HeapTree.root

        for guest_str in new_guest_list:
            parts = guest_str.split('/')
            list_value = []
            walk = 0  # เก็บค่า W แยก

            for part in parts:
                k, v = part.split()
                v = int(v)
                if k.upper() == 'WALK' or k.upper() == 'W':
                    walk = v
                else:
                    list_value.append(v)

            guest_template = tuple(list_value) 

            for w in range(walk):  
                guest_tuple = guest_template + (w,) 
                root = self.add_new_guest(
                    root=root,
                    guest_info=guest_tuple,
                )

    def add_room_manual(self, room_number: int):
        if self.Hash_table.get(room_number) is None:
            self.Hash_table.insert(room_number, "Manual Add")
            self.HeapTree.add(self.HeapTree.root, room_number)
            print(f"✅ Room {room_number} added successfully.")
            return room_number

        print(f"⚠️ Room {room_number} already exists: {self.Hash_table.get(room_number)}")
        while True:
            choice = input(
                "Collision detected. Choose an action:\n"
                "  [S]kip  : Do not add this room\n"
                "  [M]ove  : Reassign ALL existing guests, then place THIS guest here\n"
                "👉 Enter S or M: "
            ).strip().lower()

            if choice in ("s", "skip"):
                print("🚫 Skipped adding this room.")
                return None

            if choice in ("m", "move"):
                print("🔄 Reassigning all existing guests to new room numbers...")
                self.manage_current_guest()

                if self.Hash_table.get(room_number) is not None:
                    prev = self.Hash_table.get(room_number)
                    self.Hash_table.delete(room_number)
                    self.HeapTree.root, _ = self.HeapTree._delete(self.HeapTree.root, room_number)
                    print(f"ℹ️ Force-freed room {room_number} (previous occupant: {prev}).")

                self.Hash_table.insert(room_number, "Manual Add (after reassign)")
                self.HeapTree.add(self.HeapTree.root, room_number)
                print(f"✅ Room {room_number} assigned to the new manual guest after reassignment.")
                return room_number

            print("❗ Invalid input. Please type only 'S' or 'M'.")
    
    def delete_room_manual(self,room_number : int):
        deleted_hash = self.Hash_table.delete(room_number)
        deleted_tree = self.HeapTree.delete(room_number)
        if deleted_hash or deleted_tree:
            return room_number
        else:
            return f"Not found room {room_number}"
            
    def sort_room(self):
        return self.HeapTree.InOrder()
    
    def search_room_by_number(self,room_number : int):
        return self.Hash_table.get(room_number)

    def get_memory_used(self):
        return f"\n📊 Memory usage: {process.memory_info().rss / 1024**2:.2f} MB"
    def save_to_excel(self, filename="guest_list.xlsx"):
        data = []

        for node in self.HeapTree.InOrder():
            room_number = node.data
            guest_info = self.Hash_table.get(room_number)
            print_guest_info = None
            
            if guest_info is None:
                continue

            elif guest_info == 0:
                print_guest_info = "Old Guest"
            elif guest_info == 1:
                print_guest_info = "New Guest"
            else:
                print_guest_info = "Manual Add (after reassign)"
            # แปะ guest_info ดิบ ๆ ลงไปเลย
            data.append({
                "Room Number": room_number,
                "Guest Info": print_guest_info
            })

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"✅ Data saved to {filename} (raw guest_info version)")

Hotel1 = Hotel()

process = psutil.Process(os.getpid())
print(f"เริ่มต้นใช้หน่วยความจำ: {process.memory_info().rss / 1024**2:.2f} MB")

user_input = input("Enter guest first group : " ).strip()
new_guest = [x.strip() for x in user_input.split(',')]

start_time = time.perf_counter()
Hotel1.manage_new_guest(new_guest)
end_time = time.perf_counter()

print(f"✅ Guest(s) added. Execution time: {end_time - start_time:.8f} seconds")

while True:
    choice = input(
        "Select Function:\n"
        "1 → Add new guest\n"
        "2 → Add manual room (reassign all)\n"
        "3 → Delete a room\n"
        "4 → Show all room numbers (sorted)\n"
        "5 → Search guest by room number\n"
        "6 → Save data to file\n"
        "7 → Get memory used\n"
        "0 → Exit\n"
        "👉 Your choice: "
    ).strip()

    if choice == "0":
        print("Exiting program...")
        break

    # 🧩 Add new guest
    elif choice == "1":
        user_input = input("Enter new guests : ").strip()
        new_guest = [x.strip() for x in user_input.split(',')]
        
        start_time = time.perf_counter()
        Hotel1.manage_new_guest(new_guest)
        end_time = time.perf_counter()
        print(f"✅ Guest(s) added. Execution time: {end_time - start_time:.8f} seconds")

    # 🏠 Add new rooms (reassign all guests)
    elif choice == "2":
        start_time = time.perf_counter()
        room_number = input("Enter the room number to add :")
        Hotel1.add_room_manual(int(room_number))
        end_time = time.perf_counter()
        print(f"✅ Room reassignment completed. Time: {end_time - start_time:.8f} seconds")

    # ❌ Delete a room
    elif choice == "3":
        room_num = input("Enter the room number to delete: ")
        start_time = time.perf_counter()
        print(f"Delete room: {Hotel1.delete_room_manual(int(room_num))}")
        end_time = time.perf_counter()
        print(f"✅ Room deleted. Execution time: {end_time - start_time:.8f} seconds")

    # 📋 Display all rooms in sorted order
    elif choice == "4":
        print("📋 All room numbers (in order):")
        for node in Hotel1.sort_room():
            print(node.data, end=" ")
        print()

    # 🔍 Search guest by room number
    elif choice == "5":
        room_num = input("Enter room number to search: ")
        room_num = int(room_num)
        start_time = time.perf_counter()
        result = Hotel1.search_room_by_number(room_num)
        if result == "Manual Add (after reassign)":

            print(f"Result : {result}")
        elif result == 0:
            print("Old Guest")
        elif result == 1:
            print("New guest")
        else:
            print("Room not found")
        end_time = time.perf_counter()
        
        print(f"✅ Search completed. Time: {end_time - start_time:.8f} seconds")

    # 💾 Save to file
    elif choice == "6":
        start_time = time.perf_counter()
        Hotel1.save_to_excel("guest_list.xlsx")
        end_time = time.perf_counter()
        print(f"✅ Excel file saved. Time: {end_time - start_time:.8f} seconds")
    
    elif choice == "7":
        
        start_time = time.perf_counter()
        print(Hotel1.get_memory_used())
        end_time = time.perf_counter()
        print(f"✅ Guest(s) added. Execution time: {end_time - start_time:.8f} seconds")

    else:
        print("⚠️ Invalid selection. Please try again.")

    