import time
import os

from string import Template

from dotenv import load_dotenv
from keybert import KeyBERT
from pymongo import MongoClient

load_dotenv()

CONTENT_TEMPLATE = Template(
	"""
Postition: $title.
Company: $company.
Location: $location.
Description: $description.
"""
)

MAX_LENGTH = 4096

mongo_client = MongoClient(os.environ['MONGO_URI'])
db = mongo_client['linkedin']
source_collection = db['jobs']
target_collection = db['jobs_vectors']

kw_model = KeyBERT('BAAI/bge-m3')

for doc in source_collection.find():
	start_time = time.time()
	content = CONTENT_TEMPLATE.substitute(
		title=doc['title'], company=doc['company'], location=doc['location'], description=doc['description']
	)  # [:MAX_LENGTH]
	content = """
About the job

At Similarweb, we're revolutionizing the way businesses interact with the digital world by revealing to them everything that happens online. Our cutting-edge platform and unique data empower over 4,300 customers globally, including industry giants like Google, eBay, and Adidas, to make game-changing decisions that drive their digital strategies.

In 2021, we went public on the New York Stock Exchange, and we haven’t stopped growing since!

We're expanding our global presence with a brand-new site in Prague - home to Europe’s top tech talent - and seeking exceptional pioneers to help build a new dynamic team. At Similarweb, you'll innovate fast, collaborate with brilliant minds, solve big problems, work with cutting-edge technologies and data at incredible scales, and make a tangible impact on the world's most innovative companies.

We’re looking for an Experienced Backend Engineer to develop and integrate systems that retrieve, process and analyze data from around the web, in order to ensure its successful delivery to our customers.

This role will report to Team manager- R&D.

Why is this role so important at Similarweb?

Similarweb is a data-focused company, and data is the heart of our business. As a data server developer, you will work at the company's very core, designing and implementing complex high-scale systems to retrieve and analyze data from millions of web users.

Our backend engineers are responsible for the entire data lifecycle - from our endless data lakes, through choosing the right serving methods and databases, all the way to our API services.

So, what will you be doing all day?

Your role as part of the Backend Engineer means your daily responsibilities may include:

You will be a server side developer, who is passionate about learning new technologies, handling a multitude of systems, and can fit in a small team of independent developers
Develop and integrate systems that handles more than 50k events per seconds and serve varieties of clients both mobile and desktop
Manage data pipelines over Spark/Airflow framework.
Take a major part in designing and implementing complex high scale systems using large variety of technologies
Design, code and integrate scale systems
Implement solutions in AWS cloud environment, developing CI/CD pipelines.
Constantly learn new technologies and methods and enrich other team members

This Is The Perfect Job For Someone Who

Has at least 5+ years of server-side software development experience in one or more general purpose programming languages or a Data platform engineer experience.
Experience writing and designing Object Oriented code with one or more of the OO programming languages, including but not limited to: C#, Python, etc.
Holds a BSc degree in Computer Science, a related technical field of study, or equivalent practical experience.
Experience building large scale web applications : advantage for working with Microservices architecture, AWS and databases (DynamoDB, Redis, MySQL, Elasticsearch, Columnar DBs)
Familiarity with Big Data technologies: A familiarity with Spark, Databricks and Airflow is a big advantage .
Is comfortable taking on challenges and learning new technologies, including new coding languages.
Can effectively prioritize tasks and work independently
Conveys a strong sense of ownership over the products of the team
Comfortable working in a fast-paced dynamic environment

*All Similarweb offices work in a hybrid model, so you can enjoy the flexibility of working from home with the benefits of building face to face connections with fellow Similarwebbers.*

Why You’ll Love Being a Similarwebber

 You’ll actually love the product you work with:  Our customers aren’t our only raving fans. When we asked our employees why they chose to come work at Similarweb, 99% of them said “the product.” Imagine how exciting your job is when you get to work with the most powerful digital intelligence platform in the world.

 You’ll find a home for your big ideas:  We encourage an open dialogue and empower employees to bring their ideas to the table. You’ll find the resources you need to take initiative and create meaningful change within the organization.

 We offer competitive perks & benefits:  We take your well-being seriously, and offer competitive compensation packages to all employees. We also put a strong emphasis on community, with regular team outings and happy hours.

 You can grow your career in any direction you choose:  Interested in becoming a VP or want to transition into a different department? Whether it’s Career Week, personalized coaching, or our ongoing learning solutions, you’ll find all the tools and opportunities you need to develop your career right here.

 Diversity isn’t just a buzzword:  People want to work in a place where they can be themselves. We strive to create a workplace that is reflective of the communities we serve, where everyone is empowered to bring their full, authentic selves to work. We are committed to inclusivity across race, gender, ethnicity, culture, sexual orientation, age, religion, spirituality, identity and experience. We believe our culture of equality and mutual respect also helps us better understand and serve our customers in a world that is becoming more global, more diverse, and more digital every day.

We will handle your application and information related to your application in accordance with the Applicant Privacy Policy available here .
Posted on Dec 10, 2023.
"""

	keywords = kw_model.extract_keywords(
		content, top_n=25, nr_candidates=50, keyphrase_ngram_range=(1, 2), use_maxsum=False, use_mmr=True
	)
	# print('Content:', content)
	print('Keywords:', keywords)
	print('*' * 50)
	break
