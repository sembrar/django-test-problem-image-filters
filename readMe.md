# Django test assignment

This project is my solution to the following django-web-application test assignment.

### The problem statement:
1. Image upload: Users should be able to upload images to the application. The images should be stored in a database and should be retrievable by the user.
2. Image filtering: Users should be able to apply filters to their images using OpenCV. The application should provide a list of filters that can be applied and one of them should be selected. Example of filters if you want to include:
   1. Grayscale filter
   2. Sepia filter
   3. Blur filter
   4. Edge detection filter
3. Image storage: The filtered images should be stored on disk, along with filters that was applied.
4. Image retrieval: Users should be able to view a list of the filtered images that they have uploaded, along with the filter that was applied.

## How to run this project:
1. Setting up the environment:
   1. Optionally, we may want to create a python virtual environment, so that, the packages we install are installed to that virtual environment, leaving our system python untouched. Please see how to create virtual environment [here](https://docs.python.org/3/library/venv.html) and work with it.
   1. [Django](https://www.djangoproject.com/) `pip install Django==4.1.7`
   2. [Pillow](https://pypi.org/project/Pillow/) `pip install Pillow` This is required by Django to work with Images.
   3. [OpenCV](https://opencv.org/releases/) There are two ways to install this:
      1. Either from [OpenCV releases page](https://opencv.org/releases/). For Windows, the process is, we download the exe file. Run it which extracts the contents. And then we copy cv2.pyd into python's 'Lib/site-packages' directory, along with .dll files. One thing to note is that if our python is 64 bit, we copy 64 bit bersions of cv2.pyd and the dlls, else we copy the 32 bit versions.
      2. Or from pypi, [opencv-python](https://pypi.org/project/opencv-python/) (I haven't tested this) `pip install opencv-python`
   4. [numpy](https://numpy.org/) `pip install numpy` OpenCV requires it.
2. Running the project:
   1. Then, in a command prompt, navigate to the top-directory of this project where `manage.py` resides. Please note that, if we are using a virtual environment, we need to activate it first.
   2. Now, we need to create the database tables. We do this by running the following two commands in the given order:
      1. `python manage.py makemigrations`
      2. `python manage.py migrate`
   2. Then in the command prompt, run the command `python manage.py runserver`. This launches the development server and the django based web-application is served locally.
   4. The command prompt shows the link the link at which the website is being served. Copy and paste it in a browser. From there, we can browse it like a regular website.
    
## Additional optional instruction:
The database tables (that hold users, uploaded image paths, etc) can be seen and edited in the admin page. However, an admin account must be created first, with the command `python manage.py createsuperuser`. Then we can login to admin page (whose link is `/admin/` appended to the above link, i.e. the link shown in the command prompt when 'runserver' command was run)

## Demonstration of the project:
I have made a series of comments and gifs to demonstrate the working of this project [here](demonstration/demonstration.md).
