# CP-DEV-DSA

A Django based web application to bring multiple platforms like Leetcode, Codeforces, Codechef & more at one place.

## Installation
This app requires python to run on your server/localhost.

### 1. Clone the project on your local computer.

```sh
git clone https://github.com/Aayush5sep/CP-DEV-DSA
```

### 2. Install the dependencies and devDependencies.

```sh
pipenv install -r requirements.txt
pipenv shell
```
>Any other virtual environments may also work. 
>The requirements.txt file contains all the packages that need to be installed.

### 3. Generate  a Secret Key & other credentials.

- Create a new secret key for django with a secret key generator, like [Djecrety](https://djecrety.ir/).
- Set this secret key value for `DJANGO_KEY` in .env file.


### 4. Migrate the project.
Run the following commands in terminal.
```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the project.
Run the following command in terminal to start the server.
```sh
python manage.py runserver
```

## Contributing to the Project
### 1. Fork the repository
![fork](https://drive.google.com/uc?id=1ZF_tJBjVC5PVDu5eWfTbEQjvFqNoray-)

### 2. Clone the project on your local computer.

```sh
git clone <Your-Repository-URL>
```

### 3. Add the original repository as upstream

```sh
git remote add upstream https://github.com/Aayush5sep/CP-DEV-DSA
```

### 4. Create a local branch

```sh
git checkout -b <your-branch-name>
```

### 5. Commit your changes & push to your github repo

```sh
git commit -m "<feature you have worked on>"
git push origin <your-branch-name>
```

### 6. Begin & Create the local request

Click the green Compare & pull request button to begin the pull request.
![pull](https://drive.google.com/uc?id=11_LX9-eYt8AilvlfbxQYLw0NatqzxEJm)

Complete the pull request to upstream branch
![complete-pull](https://drive.google.com/uc?id=1iMrWJyos5AOTjMziQNB3yTZGuakrIe_0)






> Check out more projects by `Aayush Goyal` at [Aayush5sep][aayush]




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen)

   [git-repo]: <https://github.com/Aayush5sep/UserAuthAPI>
   [aayush]: <https://github.com/Aayush5sep>
