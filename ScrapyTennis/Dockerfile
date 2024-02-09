FROM python:3.11.5

# Set working directory
WORKDIR /app

# Copy requirements.txt files to directory
COPY ./ScrapyTennis/requirements.txt /app/
#COPY requirements.txt ./

# Install Python dependencies for scrapy
RUN pip install -r /app/requirements.txt
#RUN pip install -r requirements.txt

# Copy Scrapy project
COPY ./ScrapyTennis /app/ScrapyTennis
COPY ./scrapy.cfg /app/

# Change working directory
WORKDIR /app/ScrapyTennis

#COPY . .

# Run Scrapy script
CMD scrapy crawl lequipe && python merge_csv.py && python mongo.py
#CMD ["scrapy", "crawl", "lequipe"]; 

#CMD ["python", "merge_csv.py"]; CMD ["python", "/Mongo/mongo.py"]
