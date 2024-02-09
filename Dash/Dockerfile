FROM python:3.11.5

# Set working directory
WORKDIR /app

# Copy requirements.txt files to directory
COPY ./Dash/requirements.txt /app/

# Install Python dependencies for scrapy
RUN pip install -r requirements.txt

COPY ./Dash /app/Dash

WORKDIR /app/Dash

# Exposer le port utilisé par l'application Dash
EXPOSE 8050

# Commande pour lancer l'application
CMD ["python", "dashboard.py"]