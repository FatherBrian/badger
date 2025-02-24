## 🤝 Contributing
We welcome contributions! Please follow these steps to get started:

### **1️⃣ Setting Up Your Development Environment**
1. **Fork the repository** on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/fatherbrian/badger.git
   cd badger
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests to verify setup:
   ```bash
   pytest
   ```

### **2️⃣ Making Contributions**
- **Report Issues**: Found a bug? Open an [issue]
- **Feature Requests**: Suggest enhancements in [discussions]
- **Code Contributions**:
  1. Create a new branch:
     ```bash
     git checkout -b feature/your-feature-name
     ```
  2. Make changes and commit:
     ```bash
     git commit -m "Added new feature"
     ```
  3. Push your changes:
     ```bash
     git push origin feature/your-feature-name
     ```
  4. Open a Pull Request (PR) against the `main` branch.

### **3️⃣ Coding Standards**
- Follow **PEP8** coding style.
- Run `black` for formatting:
  ```bash
  black .
  ```
- Lint your code with:
  ```bash
  flake8
  ```

### **4️⃣ Running Tests**
We use `pytest` for testing:
```bash
pytest
```
Ensure all tests pass before submitting a PR.

