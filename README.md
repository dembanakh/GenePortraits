
# GenePortraits

A web application for generating frequency portraits (and other types of portraits in the future) of gene sequences, with some customization options.
Portraits generated by an unlogged user (guest) are available in Repository section with some limitations until their web session expires.
On the other hand, portraits generated by registered users are stored persistently.

# Technical Details

This is a **Django** application, hosted on **Heroku** platform.
- **Django-auth** is responsible for authorizing users.
- **SQLite** is exploited to store portraits persistently.
- A portrait is generated on fractal basis from a gene sequence, which is fetched from [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/) database based on a short gene ID using python **requests** library.

# How To Use

Visit https://gene-portraits.herokuapp.com/home. Since, for now, the app is hosted on Heroku, the first page loading may take a while.

# How To Build

Python v3.8 recommended.

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver` to start up a localhost development server
4. Visit http://127.0.0.1:8000/
