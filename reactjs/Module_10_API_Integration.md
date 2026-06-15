# 📥 Module 10: API Integration

Integrating backends requires fetching data asynchronously, managing loading/error states, and making clean HTTP requests using standard APIs or library wrappers.

---

## 🆚 Fetch API vs. Axios

### 📋 Feature Matrix

| Feature | Fetch API (Browser Native) | Axios (External Library) |
| :--- | :--- | :--- |
| **JSON Transformation** | Manual parsing (`res.json()`) | Automatic conversion (`response.data`) |
| **HTTP Error Handling** | Resolves on 404/500 (must check `res.ok`) | Rejects automatically on bad statuses ($<200$ or $\ge 300$) |
| **Timeout Configuration**| Needs `AbortController` setup | Easy inline timeout property configuration |
| **Interceptors** | Requires overriding global fetch | Built-in request/response interceptor pipeline |

---

## 💻 HTTP Operations (GET, POST, PUT, DELETE)

Below is a complete REST resource manager illustrating all HTTP operations using `fetch`:

```jsx
import { useState } from 'react';

function ProductDashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // 1. GET Operation
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch('https://api.site.com/products');
      if (!res.ok) throw new Error('Failed to fetch products');
      const products = await res.json();
      setData(products);
    } catch (err) {
      console.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 2. POST Operation
  const addProduct = async (newProduct) => {
    try {
      const res = await fetch('https://api.site.com/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProduct)
      });
      const data = await res.json();
      setData(prev => [...prev, data]);
    } catch (err) {
      console.error(err.message);
    }
  };

  // 3. PUT (Update) Operation
  const updatePrice = async (id, updatedPrice) => {
    try {
      const res = await fetch(`https://api.site.com/products/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ price: updatedPrice })
      });
      const data = await res.json();
      setData(prev => prev.map(p => p.id === id ? { ...p, price: data.price } : p));
    } catch (err) {
      console.error(err.message);
    }
  };

  // 4. DELETE Operation
  const deleteProduct = async (id) => {
    try {
      const res = await fetch(`https://api.site.com/products/${id}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        setData(prev => prev.filter(p => p.id !== id));
      }
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div>
      <button onClick={fetchProducts} disabled={loading}>
        {loading ? 'Loading...' : 'Load Products'}
      </button>
      {/* Product list rendering code */}
    </div>
  );
}
```

---

## 🛡️ Writing a Custom API Fetching Hook (`useFetch`)

A reusable custom hook simplifies data loading logic across multiple components and cancels requests on unmount.

```jsx
import { useState, useEffect } from 'react';

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const abortController = new AbortController();
    const { signal } = abortController;

    async function executeRequest() {
      try {
        setLoading(true);
        const response = await fetch(url, { signal });
        if (!response.ok) {
          throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    }

    executeRequest();

    // Clean up: Abort fetch if component is unmounted during API call
    return () => abortController.abort();
  }, [url]);

  return { data, loading, error };
}
```

---

🔗 **[Back to Course Index](./React_Course_Index.md)** | **[Proceed to Module 11](./Module_11_Auth_Security.md)**
