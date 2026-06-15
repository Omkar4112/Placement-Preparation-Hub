# 📝 Module 5: Handling Forms & User Input

Forms are critical for collecting user data. In React, form inputs are typically handled using **Controlled Components** where React state is the single source of truth, though **Uncontrolled Components** can be used for simpler use cases.

---

## 🛠️ Controlled vs. Uncontrolled Components

### 📋 Comparison Matrix

| Feature | Controlled Component | Uncontrolled Component |
| :--- | :--- | :--- |
| **State Source** | React State (`useState`) | Browser DOM node ref (`useRef`) |
| **Data Pulling** | Real-time on keystroke | Only on demand (e.g. form submit) |
| **Validation** | Easy real-time validations | Validated only after submission |
| **Performance** | Causes re-render on every keystroke | Only triggers layout on submission |
| **Complexity** | More boilerplate code | Less boilerplate code |

---

## 💻 Managing Multi-Input Forms with One State Object

Instead of declaring ten `useState` variables for ten form fields, configure a single object state and reference inputs by their `name` attribute.

```jsx
import { useState } from 'react';

function RegisterForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    subscribe: false
  });
  const [errors, setErrors] = useState({});

  const handleInputChange = (event) => {
    const { name, value, type, checked } = event.target;
    // Compute input value based on checkbox vs standard input type
    const inputValue = type === 'checkbox' ? checked : value;

    setFormData(prev => ({
      ...prev,
      [name]: inputValue
    }));
  };

  const handleValidationAndSubmit = (e) => {
    e.preventDefault();
    let formErrors = {};

    if (formData.username.length < 3) {
      formErrors.username = "Username must be at least 3 characters.";
    }
    if (!formData.email.includes("@")) {
      formErrors.email = "Please enter a valid email address.";
    }

    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
    } else {
      setErrors({});
      console.log("Form successfully submitted!", formData);
    }
  };

  return (
    <form onSubmit={handleValidationAndSubmit} className="form-card">
      <div>
        <label>Username:</label>
        <input 
          name="username" 
          value={formData.username} 
          onChange={handleInputChange} 
        />
        {errors.username && <span className="error">{errors.username}</span>}
      </div>

      <div>
        <label>Email:</label>
        <input 
          name="email" 
          type="email"
          value={formData.email} 
          onChange={handleInputChange} 
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label>
          <input 
            type="checkbox" 
            name="subscribe" 
            checked={formData.subscribe} 
            onChange={handleInputChange} 
          />
          Subscribe to newsletters
        </label>
      </div>

      <button type="submit">Submit Form</button>
    </form>
  );
}
```

---

## ❓ Common Interview Questions
1. **When should you use Uncontrolled Components instead of Controlled ones?**
   - Use Uncontrolled components when writing quick prototypes, integrating third-party non-React UI plugins, or handling `<input type="file" />` (which is always uncontrolled in React).

---

🔗 **[Back to Course Index](./React_Course_Index.md)** | **[Proceed to Module 6](./Module_06_Lifting_State.md)**
