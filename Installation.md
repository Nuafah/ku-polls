## Installation Guide

> Note : if the command below doesn't work try using **python3** and **pip3** instead.

1. Clone My repository from GitHub to your pc.
    ```
    git clone https://github.com/Nuafah/ku-polls.git
    ```
2. Change directory to ku-polls.
    ```
    cd  ku-polls
    ```
3. Create virtual environment.
    ```
   python -m venv venv
   ```
4. Start the virtual environment.
   * Windows
   ```
   venv\Scripts\activate
   ```
   * macOS / Linux
   ```
   . venv/bin/activate 
   ```
   
5. Install dependencies.
   ```
   pip install -r requirements.txt
   ```
   
6. Set values for externalized variables.
   * Windows
     ```
     copy sample.env .env
     ```
   * macOS / Linux
     ```
     cp sample.env .env 
     ```
     
7. Migrate.
   ``` 
   python manage.py migrate
   ```
8. Run test.
   ``` 
   python manage.py test polls
   ```
   > Note : There are 20 tests, All of them should be passed.

9. Load data.
   ``` 
   python manage.py loaddata data/users.json data/polls.json
   ```

   