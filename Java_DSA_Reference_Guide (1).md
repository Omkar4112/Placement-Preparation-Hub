# Java DSA Complete Reference Guide
### Syntax, Key Points & Problem-Solving Notes for 44 Core Topics

---

## 1. Arrays

**Declaration & Init**
```java
int[] arr = new int[5];               // default 0s
int[] arr2 = {1, 2, 3, 4, 5};
int[][] grid = new int[3][4];         // 2D array
int[][] grid2 = {{1,2},{3,4}};
```
**Key Points**
- Fixed size, O(1) index access, O(n) insert/delete (shifting needed).
- `Arrays.sort(arr)` — O(n log n), dual-pivot quicksort for primitives (not stable).
- `Arrays.sort(arr, from, to)` — sort a range.
- `Arrays.fill(arr, val)`, `Arrays.copyOf(arr, newLen)`, `Arrays.copyOfRange(arr, from, to)`.
- `Arrays.equals(a, b)`, `Arrays.toString(arr)` for printing.
- To sort in descending order (Integer[] only, not int[]): `Arrays.sort(arr, Collections.reverseOrder())`.
- For 2D sort by column: `Arrays.sort(grid, (a, b) -> a[0] - b[0]);`
- **Gotcha**: `int[]` cannot use custom comparators — must convert to `Integer[]` or use index-sort tricks.

---

## 2. Strings

**Declaration & Init**
```java
String s = "hello";
String s2 = new String("hello");      // avoid; creates new object unnecessarily
char[] chars = s.toCharArray();
String joined = String.join(",", "a", "b", "c");
```
**Key Points**
- Strings are **immutable** — every concatenation creates a new object → use `StringBuilder` in loops.
- `s.charAt(i)`, `s.length()`, `s.substring(start, end)` (end exclusive), `s.equals()` (never `==` for value comparison).
- `s.split(regex)`, `s.trim()`, `s.strip()`, `s.toLowerCase()/toUpperCase()`.
- `s.indexOf(ch)`, `s.contains()`, `s.startsWith()`, `s.endsWith()`.
- String pool: literals are cached; `new String()` bypasses pool.
- Compare with `s1.compareTo(s2)` for lexicographic ordering.
- Convert: `String.valueOf(123)`, `Integer.parseInt(s)`, `Character.toString(c)`.

---

## 3. StringBuilder

**Declaration & Use**
```java
StringBuilder sb = new StringBuilder();
sb.append("abc").append(123);
sb.insert(0, "X");
sb.deleteCharAt(0);
sb.reverse();
sb.setCharAt(0, 'Z');
String result = sb.toString();
```
**Key Points**
- Mutable, O(1) amortized append vs O(n) for String concat.
- Use whenever building strings inside a loop.
- `sb.length()`, `sb.charAt(i)`, `sb.delete(start, end)`.
- Reversing a string: `new StringBuilder(s).reverse().toString()`.

---

## 4. Character Class

**Common Static Methods**
```java
Character.isDigit(c);
Character.isLetter(c);
Character.isLetterOrDigit(c);
Character.isUpperCase(c); Character.isLowerCase(c);
Character.toUpperCase(c); Character.toLowerCase(c);
Character.isWhitespace(c);
int digit = c - '0';         // char to int digit
char ch = (char)('a' + 3);   // int to char
```
**Key Points**
- Char arithmetic works directly: `'a' + 1 == 'b'` (as int), cast back with `(char)`.
- Useful for anagram/frequency problems: index into array via `c - 'a'` (0–25).
- Always check `isLetter`/`isDigit` before arithmetic to avoid bugs with mixed input.

---

## 5. HashMap

**Declaration & Use**
```java
HashMap<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.get("a");                          // null if absent
map.getOrDefault("a", 0);
map.containsKey("a");
map.remove("a");
map.put("a", map.getOrDefault("a", 0) + 1);   // frequency counting idiom
for (Map.Entry<String, Integer> e : map.entrySet()) { e.getKey(); e.getValue(); }
map.merge("a", 1, Integer::sum);       // cleaner increment
```
**Key Points**
- O(1) average put/get/remove; O(n) worst case (hash collisions, rare).
- No ordering guarantee — use `LinkedHashMap` for insertion order, `TreeMap` for sorted keys.
- Iterate keys: `map.keySet()`; values: `map.values()`.
- `computeIfAbsent(key, k -> new ArrayList<>())` — great for building adjacency lists / grouping.
- Never mutate map while iterating with a for-each (use `Iterator.remove()` instead).

---

## 6. HashSet

**Declaration & Use**
```java
HashSet<Integer> set = new HashSet<>();
set.add(5); set.remove(5); set.contains(5);
set.size(); set.isEmpty();
LinkedHashSet<Integer> ordered = new LinkedHashSet<>();  // preserves insertion order
TreeSet<Integer> sorted = new TreeSet<>();               // sorted, O(log n) ops
```
**Key Points**
- O(1) average add/remove/contains — ideal for "have I seen this before" (duplicates, visited nodes).
- `TreeSet` extras: `first()`, `last()`, `higher(x)`, `lower(x)`, `ceiling(x)`, `floor(x)`.
- Set operations: `setA.retainAll(setB)` (intersection), `removeAll` (difference), `addAll` (union).

---

## 7. ArrayList

**Declaration & Use**
```java
ArrayList<Integer> list = new ArrayList<>();
list.add(1); list.add(0, 5);          // insert at index
list.get(0); list.set(0, 10); list.remove(0);
list.size(); list.isEmpty(); list.contains(5);
Collections.sort(list);
Collections.sort(list, (a, b) -> b - a);   // descending
Integer[] arr2 = list.toArray(new Integer[0]);
List<Integer> fromArr = Arrays.asList(1,2,3);  // fixed-size, backed by array
```
**Key Points**
- Dynamic array, amortized O(1) `add` at end, O(n) insert/remove at arbitrary index.
- Autoboxing overhead: `ArrayList<Integer>` boxes each int — costlier than `int[]` for hot loops.
- `Collections.reverse(list)`, `Collections.max/min(list)`, `Collections.frequency(list, val)`.
- 2D list: `List<List<Integer>> result = new ArrayList<>();` then `result.add(new ArrayList<>());`

---

## 8. Linked List

**Custom Node**
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}
```
**Java Built-in**
```java
LinkedList<Integer> list = new LinkedList<>();
list.addFirst(1); list.addLast(2); list.removeFirst(); list.removeLast();
list.peekFirst(); list.peekLast();
```
**Key Points**
- O(1) insert/delete at known node (vs O(n) shifting in arrays); O(n) random access.
- Classic patterns: **dummy head node** to simplify edge cases, **fast & slow pointers** (cycle detection/middle), reversing via three pointers (`prev`, `curr`, `next`).
- Always null-check before dereferencing `.next`.
- `LinkedList` implements both `List` and `Deque` — usable as a stack/queue too.

---

## 9. Stack

**Declaration & Use**
```java
Deque<Integer> stack = new ArrayDeque<>();   // preferred over java.util.Stack
stack.push(1);
stack.pop();
stack.peek();
stack.isEmpty();
```
**Key Points**
- LIFO. Use `ArrayDeque` (faster, not synchronized) instead of legacy `Stack` class.
- Classic uses: balanced parentheses, expression evaluation, next-greater-element, DFS iterative traversal, backtracking undo.
- `ArrayDeque` cannot store `null`.

---

## 10. Queue

**Declaration & Use**
```java
Queue<Integer> queue = new LinkedList<>();   // or ArrayDeque
queue.offer(1);      // add to tail
queue.poll();        // remove from head (null if empty)
queue.peek();        // view head
```
**Key Points**
- FIFO. Prefer `ArrayDeque` over `LinkedList` for queue ops — better cache locality, no node overhead.
- Core use: BFS traversal, level-order tree traversal, task scheduling.
- `poll()`/`peek()` return `null` on empty (no exception) vs `remove()`/`element()` which throw.

---

## 11. Deque (Double-Ended Queue)

**Declaration & Use**
```java
Deque<Integer> deque = new ArrayDeque<>();
deque.addFirst(1); deque.addLast(2);
deque.removeFirst(); deque.removeLast();
deque.peekFirst(); deque.peekLast();
```
**Key Points**
- Insert/remove O(1) from both ends. Backs both stack and queue implementations.
- Essential for **sliding window maximum** (monotonic deque) and **palindrome checks**.
- Prefer over `LinkedList` for performance.

---

## 12. Priority Queue (Heap)

**Declaration & Use**
```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();               // min-heap default
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<int[]> custom = new PriorityQueue<>((a, b) -> a[0] - b[0]);
minHeap.offer(5); minHeap.poll(); minHeap.peek();
```
**Key Points**
- O(log n) insert/remove, O(1) peek min/max. Backed by binary heap array internally.
- No `contains`/`remove(x)` efficiently — O(n) for those (rarely used).
- Common uses: Top-K elements, Dijkstra's algorithm, merge K sorted lists, median finder (two heaps).
- For max-heap of custom objects: comparator `(a, b) -> b.val - a.val`.

---

## 13. Recursion

**Template**
```java
void recurse(int n) {
    if (n == 0) return;             // base case — MUST exist
    // do work
    recurse(n - 1);                 // recursive case, moving toward base case
}
```
**Key Points**
- Every recursive function needs: base case(s) + progress toward base case.
- Watch stack depth — Java default stack can overflow around ~10,000–50,000 deep recursion.
- Space complexity includes call stack: O(depth).
- Tail recursion is NOT optimized by JVM (unlike some functional languages) — convert to iteration if depth is large.
- Trace with a call tree/recursion tree diagram for correctness on DP/backtracking problems.

---

## 14. Backtracking

**Template**
```java
void backtrack(List<Integer> path, int[] nums, boolean[] used, List<List<Integer>> result) {
    if (path.size() == nums.length) {
        result.add(new ArrayList<>(path));   // must copy! path is mutated later
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        path.add(nums[i]);
        backtrack(path, nums, used, result);
        path.remove(path.size() - 1);        // undo — the core backtracking step
        used[i] = false;
    }
}
```
**Key Points**
- Pattern: **choose → explore → un-choose**. Undo step is what distinguishes it from plain recursion.
- Always copy mutable state (`new ArrayList<>(path)`) before adding to results.
- Prune early (add `if` conditions before recursing) to cut search space — critical for performance.
- Common problems: permutations, combinations, subsets, N-Queens, Sudoku solver, word search.

---

## 15. Sorting

**Built-in**
```java
Arrays.sort(arr);                          // primitives: dual-pivot quicksort, O(n log n), NOT stable
Arrays.sort(objArr);                        // objects: TimSort, O(n log n), stable
Collections.sort(list, comparator);
Arrays.sort(arr, (a, b) -> a - b);          // only works on object arrays (Integer[])
```
**Key Points**
- Know complexities: Bubble/Insertion/Selection O(n²); Merge/Heap/Quick O(n log n) avg; Quick worst O(n²).
- Merge sort is stable & O(n log n) worst-case guaranteed — good for linked lists too.
- Custom comparator: `Comparator.comparingInt(x -> x.val).thenComparing(...)`.
- Counting sort / bucket sort: O(n+k) when range k is small — useful for frequency-based problems.

---

## 16. Binary Search

**Template**
```java
int lo = 0, hi = arr.length - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;         // avoids overflow vs (lo+hi)/2
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;   // not found
```
**Key Points**
- Requires sorted (or monotonic-property) array. O(log n).
- `Arrays.binarySearch(arr, target)` built-in — returns negative if not found.
- Variants: search for leftmost/rightmost occurrence, "binary search on answer" (search over a range of possible answers, not array indices) — common in optimization problems.
- Watch loop invariants carefully: `lo <= hi` vs `lo < hi`, and whether `mid` is included/excluded.

---

## 17. Two Pointers

**Template**
```java
int left = 0, right = arr.length - 1;
while (left < right) {
    if (condition) left++;
    else right--;
}
```
**Key Points**
- O(n) instead of O(n²) brute force — pointers move inward or same-direction based on condition.
- Requires sorted array typically (pair sum, container with most water) or same-direction (remove duplicates, merge two sorted arrays).
- Common problems: two-sum in sorted array, palindrome check, trapping rain water, partition (Dutch flag).

---

## 18. Sliding Window

**Template (variable size)**
```java
int left = 0, sum = 0;
for (int right = 0; right < arr.length; right++) {
    sum += arr[right];
    while (sum > target) {           // shrink window
        sum -= arr[left];
        left++;
    }
    // window [left, right] is now valid — process it
}
```
**Key Points**
- O(n) for substring/subarray problems that would otherwise be O(n²).
- Fixed-size window: maintain size `k` by removing `arr[right-k]` when `right >= k`.
- Track window state with a HashMap/frequency array for "longest substring with K distinct chars" type problems.
- Pair naturally with Deque for max/min-in-window problems.

---

## 19. Prefix Sum

**Template**
```java
int[] prefix = new int[arr.length + 1];
for (int i = 0; i < arr.length; i++) prefix[i+1] = prefix[i] + arr[i];
// sum of range [i, j] inclusive:
int rangeSum = prefix[j+1] - prefix[i];
```
**Key Points**
- Precompute in O(n), answer any range-sum query in O(1) — huge win over repeated O(n) summation.
- 2D prefix sum for submatrix sum queries: `prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + matrix[i-1][j-1]`.
- Prefix XOR / prefix product follow the same idea for different operations.
- Combine with HashMap for "subarray sum equals K" (store prefix sums seen so far).

---

## 20. Bit Manipulation

**Common Operations**
```java
a & b, a | b, a ^ b, ~a;
a << n, a >> n, a >>> n;               // >>> is unsigned right shift
a & 1;                                  // check if odd
a & (a - 1);                            // clear lowest set bit
a | (1 << i);                           // set bit i
a & ~(1 << i);                          // clear bit i
a ^ (1 << i);                           // toggle bit i
(a & (1 << i)) != 0;                    // check bit i
Integer.bitCount(a);                    // count set bits
Integer.toBinaryString(a);
```
**Key Points**
- XOR trick: `a ^ a == 0`, `a ^ 0 == a` — used to find single non-duplicate number.
- `n & (n-1) == 0` checks power of two (n > 0).
- Bitmasking used for subset enumeration: iterate `mask` from `0` to `(1<<n)-1` to represent all subsets.
- Java ints are 32-bit signed — be careful with sign bit in shifts (`>>` sign-extends, `>>>` doesn't).

---

## 21. Greedy Algorithms

**Key Points**
- Make the locally optimal choice at each step, hoping it leads to global optimum — works only when the **greedy-choice property** and **optimal substructure** hold.
- No fixed syntax template — pattern is: sort by some criterion, then iterate making the best immediate choice.
- Common problems: activity selection/interval scheduling (sort by end time), Huffman coding, coin change (only works greedily for canonical coin systems), Jump Game, gas station.
- Always sanity check with a counterexample — greedy is wrong more often than DP for tricky constraints; if greedy fails, consider DP.

---

## 22. Trees

**Node Definition**
```java
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}
```
**Traversals**
```java
void preorder(TreeNode n) { if (n==null) return; visit(n); preorder(n.left); preorder(n.right); }
void inorder(TreeNode n)  { if (n==null) return; inorder(n.left); visit(n); inorder(n.right); }
void postorder(TreeNode n){ if (n==null) return; postorder(n.left); postorder(n.right); visit(n); }
```
**Key Points**
- Recursive traversals are O(n) time, O(h) space (h = height, worst case O(n) for skewed tree).
- Level-order (BFS) uses a Queue instead of recursion.
- Always null-check the root/node first.
- Height/diameter/balanced-check problems: compute bottom-up, return info via helper function.

---

## 23. Binary Search Trees (BST)

**Key Points**
- Invariant: left subtree < node < right subtree (all nodes, not just direct children).
- Search/insert/delete: O(log n) average, O(n) worst case (degenerate/skewed tree).
- **Inorder traversal of a BST yields sorted order** — key fact for validation problems.
- Validate BST: pass down `(min, max)` bounds recursively, don't just compare with immediate children.
- Deletion has 3 cases: no children (remove), one child (replace with child), two children (replace with inorder successor/predecessor, then delete that node).

---

## 24. Heaps

*(See also #12 Priority Queue — Java's heap implementation)*

**Key Points**
- Complete binary tree stored as an array; parent at `i`, children at `2i+1` and `2i+2`.
- Min-heap: parent ≤ children. Max-heap: parent ≥ children.
- `heapify` (sift-down) is O(log n); building a heap from an array is O(n) total (not O(n log n)).
- `PriorityQueue` in Java IS a heap — use it directly rather than hand-rolling unless the problem demands custom array-based heap manipulation (like in-place heap sort).

---

## 25. Tries

**Implementation**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEnd;
}
class Trie {
    TrieNode root = new TrieNode();
    void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.isEnd = true;
    }
    boolean search(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return node.isEnd;
    }
}
```
**Key Points**
- O(L) insert/search where L = word length — independent of number of words stored.
- Great for: autocomplete, prefix search, word search boards, longest common prefix.
- Alternative: `HashMap<Character, TrieNode> children` if alphabet is large/sparse (Unicode) instead of fixed array.

---

## 26. Graphs

**Representations**
```java
// Adjacency list (most common)
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
graph.get(u).add(v);          // directed edge u -> v
graph.get(v).add(u);          // add both directions for undirected

// Adjacency matrix
int[][] matrix = new int[n][n];
matrix[u][v] = 1;
```
**Key Points**
- Adjacency list: O(V+E) space, efficient for sparse graphs. Matrix: O(V²) space, O(1) edge lookup.
- Weighted graphs: store `List<int[]>` where each `int[]` is `{neighbor, weight}`.
- Track `visited[]` array/set to avoid infinite loops in cyclic graphs.

---

## 27. BFS (Breadth-First Search)

**Template**
```java
Queue<Integer> queue = new LinkedList<>();
boolean[] visited = new boolean[n];
queue.offer(start);
visited[start] = true;
while (!queue.isEmpty()) {
    int node = queue.poll();
    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) {
            visited[neighbor] = true;
            queue.offer(neighbor);
        }
    }
}
```
**Key Points**
- Explores level by level — guarantees **shortest path in unweighted graphs**.
- Mark visited when **enqueuing**, not when dequeuing, to avoid duplicate enqueues.
- Track distance/level with a parallel array or by storing `(node, dist)` pairs, or process queue in batches ("level" variable).

---

## 28. DFS (Depth-First Search)

**Recursive Template**
```java
void dfs(int node, boolean[] visited, List<List<Integer>> graph) {
    visited[node] = true;
    // process node
    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) dfs(neighbor, visited, graph);
    }
}
```
**Iterative (using Stack)**
```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(start);
while (!stack.isEmpty()) {
    int node = stack.pop();
    if (visited[node]) continue;
    visited[node] = true;
    for (int neighbor : graph.get(node)) stack.push(neighbor);
}
```
**Key Points**
- Explores as deep as possible before backtracking — good for connectivity, cycle detection, topological sort, path existence.
- For cycle detection in **directed** graphs, need 3 states (unvisited/visiting/visited) not just boolean visited.
- Recursive DFS risks stack overflow on deep/large graphs — use iterative version for large inputs.

---

## 29. Topological Sort

**Kahn's Algorithm (BFS-based, using in-degrees)**
```java
int[] indegree = new int[n];
for (List<Integer> adj : graph) for (int v : adj) indegree[v]++;
Queue<Integer> queue = new LinkedList<>();
for (int i = 0; i < n; i++) if (indegree[i] == 0) queue.offer(i);
List<Integer> order = new ArrayList<>();
while (!queue.isEmpty()) {
    int node = queue.poll();
    order.add(node);
    for (int neighbor : graph.get(node)) {
        if (--indegree[neighbor] == 0) queue.offer(neighbor);
    }
}
// if order.size() < n, a cycle exists — no valid topological order
```
**Key Points**
- Only valid for **Directed Acyclic Graphs (DAGs)**.
- Two approaches: Kahn's (BFS + in-degree) or DFS-based (post-order push to a stack, then reverse).
- Classic use: course scheduling, build dependency resolution, task ordering.
- Detecting a cycle: if fewer than `n` nodes get processed, a cycle exists.

---

## 30. Union Find (Disjoint Set)

**Implementation**
```java
int[] parent, rank;
void init(int n) {
    parent = new int[n]; rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
}
int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);   // path compression
    return parent[x];
}
void union(int x, int y) {
    int rx = find(x), ry = find(y);
    if (rx == ry) return;
    if (rank[rx] < rank[ry]) { int t = rx; rx = ry; ry = t; }
    parent[ry] = rx;
    if (rank[rx] == rank[ry]) rank[rx]++;              // union by rank
}
```
**Key Points**
- With path compression + union by rank: near O(1) amortized per operation (technically O(α(n))).
- Used for: connected components, Kruskal's MST, cycle detection in undirected graphs, "number of islands" variants, redundant connection problems.
- Always initialize `parent[i] = i` (every node is its own root initially).

---

## 31. Dynamic Programming (DP)

**Approaches**
```java
// Top-down (memoization)
Integer[] memo = new Integer[n+1];
int fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != null) return memo[n];
    return memo[n] = fib(n-1) + fib(n-2);
}

// Bottom-up (tabulation)
int[] dp = new int[n+1];
dp[0] = 0; dp[1] = 1;
for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
```
**Key Points**
- Applies when a problem has **overlapping subproblems** + **optimal substructure**.
- Steps: (1) define state/dp array meaning clearly, (2) find recurrence relation, (3) identify base cases, (4) decide iteration order (bottom-up) or add memo cache (top-down).
- Space optimization: if `dp[i]` only depends on `dp[i-1]`/`dp[i-2]`, use rolling variables instead of a full array.
- Common patterns: knapsack (0/1, unbounded), LCS/LIS, edit distance, coin change, partition problems.

---

## 32. Intervals

**Template (merge overlapping)**
```java
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);   // sort by start
List<int[]> merged = new ArrayList<>();
for (int[] iv : intervals) {
    if (!merged.isEmpty() && iv[0] <= merged.get(merged.size()-1)[1]) {
        merged.get(merged.size()-1)[1] = Math.max(merged.get(merged.size()-1)[1], iv[1]);
    } else {
        merged.add(iv);
    }
}
```
**Key Points**
- Almost always start by **sorting** — by start time (merging) or end time (scheduling/greedy selection).
- Overlap check: `a[0] <= b[1] && b[0] <= a[1]`.
- Common problems: merge intervals, insert interval, meeting rooms (min rooms needed = max overlap, often solved with a min-heap of end times or a sweep-line + counter).

---

## 33. Monotonic Stack

**Template (next greater element)**
```java
Deque<Integer> stack = new ArrayDeque<>();   // stores indices
int[] result = new int[arr.length];
for (int i = 0; i < arr.length; i++) {
    while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
        result[stack.pop()] = arr[i];
    }
    stack.push(i);
}
```
**Key Points**
- Maintains elements in increasing or decreasing order in the stack; pops when the incoming element breaks the monotonic property.
- Each element pushed/popped at most once → O(n) total despite the nested-looking loop.
- Classic uses: next greater/smaller element, daily temperatures, largest rectangle in histogram, stock span.

---

## 34. Monotonic Queue

**Template (sliding window maximum via Deque)**
```java
Deque<Integer> deque = new ArrayDeque<>();  // stores indices, values decreasing
int[] result = new int[arr.length - k + 1];
for (int i = 0; i < arr.length; i++) {
    while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();   // remove out of window
    while (!deque.isEmpty() && arr[deque.peekLast()] < arr[i]) deque.pollLast(); // maintain decreasing order
    deque.offerLast(i);
    if (i >= k - 1) result[i - k + 1] = arr[deque.peekFirst()];
}
```
**Key Points**
- Deque (not stack) because elements must be removed from the **front** when they slide out of the window.
- O(n) total for sliding window max/min — beats the naive O(n·k).
- Front of deque always holds the current window's max (or min).

---

## 35. Math & Number Theory

**Common Utilities**
```java
Math.max(a, b); Math.min(a, b); Math.abs(a);
Math.pow(base, exp);           // returns double
Math.sqrt(x); Math.floor(x); Math.ceil(x);
long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }   // Euclidean algorithm
long lcm(long a, long b) { return a / gcd(a, b) * b; }
boolean isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; (long)i * i <= n; i++) if (n % i == 0) return false;
    return true;
}
```
**Key Points**
- Watch for **integer overflow** — use `long` for products/sums that might exceed ~2.1 billion (int max ~2^31-1).
- Sieve of Eratosthenes for finding all primes up to N in O(N log log N).
- Modular arithmetic for large numbers: `(a % MOD + b % MOD) % MOD`; be careful with negative mod results in Java (`%` can return negative).
- `Math.pow` returns a `double` — avoid for exact integer power computations; write manual fast exponentiation instead if precision matters.

---

## 36. Hashing Techniques

**Key Points**
- **Frequency counting**: `HashMap<Character/Integer, Integer>` — increment counts, compare maps for anagram-type problems.
- **Two-sum pattern**: store `value → index` in a HashMap while iterating once; check `target - current` exists — O(n) instead of O(n²).
- **Prefix sum + HashMap**: store cumulative sums seen so far to find subarrays with a target sum in O(n) (see #19).
- **Custom hashing for objects**: override both `hashCode()` and `equals()` together (never one without the other) if using custom objects as HashMap keys or in a HashSet.
- **String hashing for anagrams**: sort chars as canonical key (`Arrays.sort(charArray)`, then `new String(charArray)`), or use a 26-length frequency array as the key (via `Arrays.toString`).
- Collision handling: Java's HashMap uses buckets with linked lists (converting to red-black trees when a bucket grows large, since Java 8) — average O(1), worst-case O(log n) per bucket now instead of O(n).
- Rolling hash (like Rabin-Karp) for substring matching — compute a hash incrementally in O(1) per shift instead of recomputing.

---

## 37. Fast I/O (Reading Input)

**Scanner (simple, slower)**
```java
import java.util.Scanner;
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
long x = sc.nextLong();
double d = sc.nextDouble();
String word = sc.next();          // single token, stops at whitespace
String line = sc.nextLine();      // whole line including spaces
sc.close();
```
**BufferedReader (fast, preferred for large input)**
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
int n = Integer.parseInt(br.readLine().trim());
StringTokenizer st = new StringTokenizer(br.readLine());
int[] arr = new int[n];
for (int i = 0; i < n; i++) arr[i] = Integer.parseInt(st.nextToken());
br.close();
```
**Key Points**
- `Scanner` is convenient but slow — fine for interviews (small input), risky for competitive programming with 10^5+ lines.
- `sc.nextLine()` after `sc.nextInt()` reads an empty leftover line — call an extra `sc.nextLine()` to consume the newline, or just avoid mixing them.
- `BufferedReader` + `StringTokenizer` is the standard fast-I/O combo when performance matters.
- Wrap `readLine()`/parsing in `try-catch (IOException e)` if not declaring `throws IOException` on `main`.
- Most interview platforms (LeetCode-style) hand you a pre-filled method signature and don't need any of this — this is mainly for HackerRank/Codeforces-style stdin problems.

---

## 38. Comparable & Comparator (Custom Objects)

**Comparable — natural ordering, built into the class**
```java
class Employee implements Comparable<Employee> {
    int salary;
    Employee(int salary) { this.salary = salary; }
    @Override
    public int compareTo(Employee other) {
        return this.salary - other.salary;     // ascending by salary
    }
}
// Now Collections.sort(list) and TreeSet<Employee> work automatically.
```
**Comparator — external, flexible, multiple orderings**
```java
Comparator<Employee> bySalary = (a, b) -> a.salary - b.salary;
Comparator<Employee> bySalaryDesc = (a, b) -> b.salary - a.salary;

// Cleaner builder style, chainable, avoids overflow from subtraction:
Comparator<Employee> cmp = Comparator.comparingInt((Employee e) -> e.salary)
                                      .thenComparing(e -> e.name)
                                      .reversed();
Collections.sort(list, cmp);
list.sort(cmp);                       // equivalent, List has sort() directly
```
**Key Points**
- Use `Comparable` when there's one natural/default ordering for the class; use `Comparator` when you need multiple orderings or can't modify the class.
- **Never** subtract doubles/longs for comparators (`a.val - b.val`) if `val` can overflow `int` or is a `double` — use `Integer.compare(a, b)` / `Long.compare(a, b)` / `Double.compare(a, b)` instead.
- `Comparator.comparingInt(...).thenComparing(...)` is the safe, readable way to build multi-key comparators.
- `PriorityQueue`, `TreeMap`, `TreeSet`, `Collections.sort`, `Arrays.sort` (object arrays only) all accept a `Comparator`.

---

## 39. Dijkstra's Algorithm

**Template (min-heap based, single-source shortest path, non-negative weights)**
```java
int[] dist = new int[n];
Arrays.fill(dist, Integer.MAX_VALUE);
dist[src] = 0;
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]); // {node, dist}
pq.offer(new int[]{src, 0});

while (!pq.isEmpty()) {
    int[] curr = pq.poll();
    int node = curr[0], d = curr[1];
    if (d > dist[node]) continue;          // stale entry, skip
    for (int[] edge : graph.get(node)) {   // edge = {neighbor, weight}
        int neighbor = edge[0], weight = edge[1];
        if (dist[node] + weight < dist[neighbor]) {
            dist[neighbor] = dist[node] + weight;
            pq.offer(new int[]{neighbor, dist[neighbor]});
        }
    }
}
```
**Key Points**
- O((V+E) log V) with a binary heap. Fails on **negative weights** — use Bellman-Ford instead for those.
- The `if (d > dist[node]) continue;` line is essential — Java's `PriorityQueue` has no `decreaseKey`, so stale/outdated entries are just skipped ("lazy deletion") instead.
- Graph must be stored as adjacency list of `{neighbor, weight}` pairs (see #26 Graphs).
- Bellman-Ford (handles negative weights, detects negative cycles) relaxes all edges `V-1` times: `for (int i = 0; i < V-1; i++) for (int[] edge : edges) if (dist[edge[0]] + edge[2] < dist[edge[1]]) dist[edge[1]] = dist[edge[0]] + edge[2];`

---

## 40. Segment Tree

**Template (range sum query + point update)**
```java
int[] tree;
int n;
void build(int[] arr) {
    n = arr.length;
    tree = new int[4 * n];
    build(arr, 0, 0, n - 1);
}
void build(int[] arr, int node, int start, int end) {
    if (start == end) { tree[node] = arr[start]; return; }
    int mid = (start + end) / 2;
    build(arr, 2*node+1, start, mid);
    build(arr, 2*node+2, mid+1, end);
    tree[node] = tree[2*node+1] + tree[2*node+2];
}
void update(int node, int start, int end, int idx, int val) {
    if (start == end) { tree[node] = val; return; }
    int mid = (start + end) / 2;
    if (idx <= mid) update(2*node+1, start, mid, idx, val);
    else update(2*node+2, mid+1, end, idx, val);
    tree[node] = tree[2*node+1] + tree[2*node+2];
}
int query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;              // no overlap
    if (l <= start && end <= r) return tree[node];   // total overlap
    int mid = (start + end) / 2;                     // partial overlap
    return query(2*node+1, start, mid, l, r) + query(2*node+2, mid+1, end, l, r);
}
```
**Key Points**
- O(log n) update and range query, O(n) build — beats prefix sums when the array is **mutable**.
- Array size `4*n` is a safe upper bound for a recursive segment tree.
- Same skeleton works for range min/max/gcd — just swap the merge operation (`+` above) accordingly.
- For point-update + range-query with only sums, a **Fenwick Tree** (below) is simpler and faster in practice.

---

## 41. Fenwick Tree (Binary Indexed Tree)

**Template (1-indexed, prefix sum + point update)**
```java
int[] bit;
int n;
void init(int size) { n = size; bit = new int[n + 1]; }

void update(int i, int delta) {          // add delta at index i (1-indexed)
    for (; i <= n; i += i & (-i)) bit[i] += delta;
}
int query(int i) {                       // prefix sum [1..i]
    int sum = 0;
    for (; i > 0; i -= i & (-i)) sum += bit[i];
    return sum;
}
int rangeQuery(int l, int r) { return query(r) - query(l - 1); }
```
**Key Points**
- O(log n) update and prefix-sum query, O(n) build (or O(n log n) via repeated `update`), O(n) space — simpler and lighter than a Segment Tree for prefix-sum-style problems.
- `i & (-i)` isolates the lowest set bit — the core trick that lets it walk parent/child indices.
- Must be **1-indexed**; index 0 is unused.
- Common uses: counting inversions, dynamic range-sum queries, "range update range query" variants with extensions.

---

## 42. Matrix Traversal Directions

**Template**
```java
// 4-directional (up, down, left, right)
int[][] dirs4 = {{-1,0},{1,0},{0,-1},{0,1}};

// 8-directional (includes diagonals)
int[][] dirs8 = {{-1,0},{1,0},{0,-1},{0,1},{-1,-1},{-1,1},{1,-1},{1,1}};

for (int[] d : dirs4) {
    int nr = row + d[0], nc = col + d[1];
    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc]) {
        // valid neighbor — process it
    }
}
```
**Key Points**
- Bounds check (`0 <= nr < rows && 0 <= nc < cols`) before every access — the #1 source of `ArrayIndexOutOfBoundsException` in grid problems.
- Grid BFS/DFS (number of islands, flood fill, rotting oranges) is identical to graph BFS/DFS, just with `dirs4`/`dirs8` generating neighbors instead of an adjacency list.
- `int[][] visited = new int[rows][cols];` or `boolean[][]` — remember 2D arrays need `new int[rows][cols]`, not `new int[rows]`.

---

## 43. Java Syntax Gotchas (Interview Essentials)

**Switch statement / expression**
```java
switch (day) {
    case 1: System.out.println("Mon"); break;
    case 2: System.out.println("Tue"); break;
    default: System.out.println("Other");
}
// Modern switch expression (Java 14+):
String result = switch (day) {
    case 1 -> "Mon";
    case 2 -> "Tue";
    default -> "Other";
};
```
**Ternary operator**
```java
int max = (a > b) ? a : b;
```
**Try-catch**
```java
try {
    int x = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    // always runs, cleanup code
}
```
**Varargs**
```java
int sum(int... nums) {              // accepts 0 or more ints, treated as int[]
    int total = 0;
    for (int n : nums) total += n;
    return total;
}
```
**instanceof (pattern matching, Java 16+)**
```java
if (obj instanceof String s) {      // auto-casts to s if true
    System.out.println(s.length());
}
```
**Key Points**
- **Integer caching gotcha**: `Integer a = 127, b = 127; a == b` → `true` (cached). `Integer a = 200, b = 200; a == b` → `false` (not cached, different objects). **Always use `.equals()` for boxed `Integer`/`Long` comparison**, never `==`, unless comparing to a primitive (which auto-unboxes).
- Autoboxing in collections means `List<Integer>` comparisons via `==` are a classic silent bug — this trips people up constantly in interviews.
- `Math.floorDiv(a, b)` / `Math.floorMod(a, b)` give mathematically correct results for negative numbers, unlike `/` and `%` which truncate/round toward zero in Java.
- Array default values: `int[]` → 0, `boolean[]` → false, `Object[]`/`String[]` → null. Uninitialized array elements are never garbage values (unlike C).

---

## 44. Cloning & Copying Arrays

```java
int[] copy1 = arr.clone();                          // shallow copy, 1D — fine for primitives
int[] copy2 = Arrays.copyOf(arr, arr.length);        // same effect, resizable

// 2D arrays: .clone() only copies the outer array (rows still point to same inner arrays!)
int[][] deepCopy = new int[grid.length][];
for (int i = 0; i < grid.length; i++) {
    deepCopy[i] = grid[i].clone();                   // must clone each row separately
}
```
**Key Points**
- `grid.clone()` on a 2D array is a **shallow copy** — mutating `deepCopy[0][0]` would also mutate `grid[0][0]` if you skip the per-row clone. This is a very common bug in matrix/backtracking problems.
- For `List<List<Integer>>`, deep-copying similarly requires `new ArrayList<>(innerList)` per row, not just copying the outer list.

---

## Quick Complexity Cheat Sheet

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| ArrayList | O(1) | O(n) | O(n)* | O(n) |
| LinkedList | O(n) | O(n) | O(1) | O(1) |
| HashMap/HashSet | — | O(1)* | O(1)* | O(1)* |
| TreeMap/TreeSet | — | O(log n) | O(log n) | O(log n) |
| Stack/Queue/Deque | O(1) ends | O(n) | O(1) | O(1) |
| PriorityQueue | O(1) peek | O(n) | O(log n) | O(log n) |
| BST (balanced) | — | O(log n) | O(log n) | O(log n) |

*amortized / average case

---

## General Problem-Solving Checklist
1. Clarify constraints (n size, value ranges) — this hints at required time complexity.
2. Identify the pattern family (sorting? two pointers? graph traversal? DP?) from problem shape.
3. Start with brute force mentally, then optimize using the right data structure above.
4. Handle edge cases first: empty input, single element, duplicates, negative numbers.
5. Trace through a small example by hand before coding.
6. Check overflow (`long` vs `int`), off-by-one errors in loops/substring bounds, and null pointers.
