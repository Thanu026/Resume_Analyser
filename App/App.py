
import streamlit as st # core package used in this project
import pandas as pd
import base64, random
import time,datetime
import pymysql
import os
import socket
import platform
import geocoder
import secrets
import io,random
import plotly.express as px # to create visualisations at the admin session
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
# libraries used to parse the pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
# pre stored data for prediction purposes
from Courses import data_analyst_courses,database_administrator_courses,devops_engineer_courses,backend_development_courses,business_analyst_courses,fashion_technology_courses,full_stack_developer_courses,cloud_analyst_courses,cyber_security_analyst_courses,hr_courses,quality_assurance_courses,networking_analyst_courses,software_tester_courses,resume_videos,interview_videos
import nltk
nltk.download('stopwords')


###### Preprocessing functions ######


# Generates a link allowing the data in a given panda dataframe to be downloaded in csv format 
def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Reads Pdf file and check_extractable
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    ## close open handles
    converter.close()
    fake_file_handle.close()
    return text


# show uploaded file path to view pdf_display
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# course recommendations which has data already loaded from Courses.py
def course_recommender(course_list):
    st.subheader("Courses & Certificates Recommendations")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco = 10
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

# sql connector
connection = pymysql.connect(host='localhost',user='root',password='0129',db='logic')
cursor = connection.cursor()


# inserting miscellaneous data, fetched results, prediction and recommendation into user_data table
def insert_data(sec_token,ip_add,host_name,dev_user,os_name_ver,latlong,city,state,country,act_name,act_mail,act_mob,name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses,pdf_name):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (str(sec_token),str(ip_add),host_name,dev_user,os_name_ver,str(latlong),city,state,country,act_name,act_mail,act_mob,name,email,str(res_score),timestamp,str(no_of_pages),reco_field,cand_level,skills,recommended_skills,courses,pdf_name)
    cursor.execute(insert_sql, rec_values)
    connection.commit()


# inserting feedback data into user_feedback table
def insertf_data(feed_name,feed_email,feed_score,comments,Timestamp):
    DBf_table_name = 'user_feedback'
    insertfeed_sql = "insert into " + DBf_table_name + """
    values (0,%s,%s,%s,%s,%s)"""
    rec_values = (feed_name, feed_email, feed_score, comments, Timestamp)
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()


###### Setting Page Configuration (favicon, Logo, Title) ######


st.set_page_config(
   page_title="Resume Parsing and Skills Suggestions",
   page_icon='./Logo/recommend.png',
)


###### Main function run() ######


def run():
    
    # (Logo, Heading, Sidebar etc)
    img = Image.open('./Logo/recommend.png')
    st.image(img)
    st.sidebar.markdown("Server")
    activities = ["User", "Feedback", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    st.sidebar.markdown('''
        <!-- site visitors -->

        <div id="sfct2xghr8ak6lfqt3kgru233378jya38dy" hidden></div>

        <noscript>
            <a href="https://www.freecounterstat.com" title="hit counter">
                <img src="https://counter9.stat.ovh/private/freecounterstat.php?c=t2xghr8ak6lfqt3kgru233378jya38dy" border="0" title="hit counter" alt="hit counter"> -->
            </a>
        </noscript>
    
        <p>Visitors <img src="https://counter9.stat.ovh/private/freecounterstat.php?c=t2xghr8ak6lfqt3kgru233378jya38dy" title="Free Counter" Alt="web counter" width="60px"  border="0" /></p>
    
    ''', unsafe_allow_html=True)

    ###### Creating Database and Table ######


    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
    cursor.execute(db_sql)


    # Create table user_data and user_feedback
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                    sec_token varchar(20) NOT NULL,
                    ip_add varchar(50) NULL,
                    host_name varchar(50) NULL,
                    dev_user varchar(50) NULL,
                    os_name_ver varchar(50) NULL,
                    latlong varchar(50) NULL,
                    city varchar(50) NULL,
                    state varchar(50) NULL,
                    country varchar(50) NULL,
                    act_name varchar(50) NOT NULL,
                    act_mail varchar(50) NOT NULL,
                    act_mob varchar(20) NOT NULL,
                    Name varchar(500) NOT NULL,
                    Email_ID VARCHAR(500) NOT NULL,
                    resume_score VARCHAR(8) NOT NULL,
                    Timestamp VARCHAR(50) NOT NULL,
                    Page_no VARCHAR(5) NOT NULL,
                    Predicted_Field BLOB NOT NULL,
                    User_level BLOB NOT NULL,
                    Actual_skills BLOB NOT NULL,
                    Recommended_skills BLOB NOT NULL,
                    Recommended_courses BLOB NOT NULL,
                    pdf_name varchar(50) NOT NULL,
                    PRIMARY KEY (ID)
                    );
                """
    cursor.execute(table_sql)


    DBf_table_name = 'user_feedback'
    tablef_sql = "CREATE TABLE IF NOT EXISTS " + DBf_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                        feed_name varchar(50) NOT NULL,
                        feed_email VARCHAR(50) NOT NULL,
                        feed_score VARCHAR(5) NOT NULL,
                        comments VARCHAR(100) NULL,
                        Timestamp VARCHAR(50) NOT NULL,
                        PRIMARY KEY (ID)
                    );
                """
    cursor.execute(tablef_sql)


    ###### CODE FOR CLIENT SIDE (USER) ######

    if choice == 'User':
        
        # Collecting Miscellaneous Information
        act_name = st.text_input('Name*')
        act_mail = st.text_input('Mail*')
        act_mob  = st.text_input('Mobile Number*')
        sec_token = secrets.token_urlsafe(12)
        host_name = socket.gethostname()
        ip_add = socket.gethostbyname(host_name)
        dev_user = os.getlogin()
        os_name_ver = platform.system() + " " + platform.release()
        g = geocoder.ip('me')
        latlong = g.latlng
        geolocator = Nominatim(user_agent="http")
        location = geolocator.reverse(latlong, language='en')
        address = location.raw['address']
        cityy = address.get('city', '')
        statee = address.get('state', '')
        countryy = address.get('country', '')  
        city = cityy
        state = statee
        country = countryy


        # Upload Resume
        st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload Your Resume, And Get Smart Recommendations</h5>''',unsafe_allow_html=True)
        
        ## file upload in pdf format
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Hang On,Your Resume is Parsing'):
                time.sleep(4)
        
            ### saving the uploaded resume to folder
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            pdf_name = pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)

            ### parsing and extracting whole resume 
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                
                ## Get the whole resume data into resume_text
                resume_text = pdf_reader(save_image_path)

                ## Showing Analyzed data from (resume_data)
                st.header("**Resume Analysis ")
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic Details")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Degree: '+str(resume_data['degree']))                    
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))

                except:
                    pass
                ## Predicting Candidate Experience Level 

                ### Trying with different possibilities
                cand_level = ''
                if resume_data['no_of_pages'] < 1:                
                    cand_level = "NA"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                
                #### if internship then intermediate level
                elif 'INTERNSHIP' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'INTERNSHIPS' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'Internship' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'Internships' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                
                #### if Work Experience/Experience then Experience level
                elif 'EXPERIENCE' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'WORK EXPERIENCE' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'Experience' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'Work Experience' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!!''',unsafe_allow_html=True)


                ## Skills Analyzing and Recommendation
                st.subheader("Skills Recommendation ")
                
                ### Current Analyzed Skills
                keywords = st_tags(label='Your Current Skills',
                text='See our skills recommendation below',value=resume_data['skills'],key = '1  ')

                data_analyst_keywords = [
                    'data visualization',
                    'ETL',
                    'data cleaning',
                    'statistical analysis',
                    'business intelligence',
                    'SQL',
                    'data mining',
                    'predictive modeling',
                    'time series analysis',
                    'machine learning',
                    'natural language processing',
                    'big data technologies',
                    'data warehousing',
                    'dashboard development',
                    'reporting tools'
                ]

                database_administrator_keywords = [
                     'DDL', 'DML', 'DQL', 'TCL'
                    'database management systems',
                    'database modeling',
                    'performance tuning',
                    'backup and recovery',
                    'database security',
                    'cloud-based databases',
                    'query optimization',
                    'database replication',
                    'disaster recovery planning',
                    'database migrations',
                    'data encryption',
                    'data integrity',
                    'data archival',
                    'distributed databases',
                    'database clustering'
                ]

                devops_engineer_keywords = [
                    'automation scripting',
                    'containerization',
                    'cloud platform',
                    'continuous monitoring',
                    'log management',
                    'release management',
                    'infrastructure scaling',
                    'security automation',
                    'configuration drift detection',
                    'incident response automation',
                    'service discovery',
                    'immutable infrastructure'
                ]

                backend_developer_keywords = [
                    'backend developer',
                    'server',
                    'API',
                    'database',
                    'RESTful',
                    'Microservices',
                    'ORM',
                    'GraphQL',
                    'Docker',
                    'Kubernetes',
                    'AWS',
                    'Azure',
                    'Google Cloud Platform',
                    'authentication',
                    'authorization',
                    'web security',
                    'performance optimization',
                    'cloud-native development',
                    'message brokers',
                    'serverless computing'
                ]

                business_analyst_keywords = [
                    'requirements gathering',
                    'process modeling',
                    'data analysis',
                    'business intelligence',
                    'stakeholder management',
                    'problem-solving',
                    'project management',
                    'change management',
                    'business process reengineering',
                    'data-driven decision-making',
                    'business case development',
                    'user acceptance testing',
                    'root cause analysis',
                    'customer journey mapping',
                    'competitor analysis'
                ]

                fashion_designer_keywords = [
                    'MODARIS',
                    'ADOBE ILLUSTRATOR',
                    'MS OFFICE',
                    'MERCHANDISING',
                    'INDUSTRIAL ENGINEER',
                    'QUALITY',
                    'creativity',
                    'fashion sketching',
                    'fabrics and textiles',
                    'sewing and garment construction',
                    'color theory',
                    'trend awareness',
                    'attention to detail',
                    'communication skills',
                    'business acumen',
                    'adaptability',
                    'resilience'
                ]


                full_stack_developer_keywords = [
                    'full stack developer',
                    'web development',
                    'backend development',
                    'frontend development',
                    'testing',
                    'Git',
                    'CI/CD',
                    'containerization',
                    'DevOps',
                    'agile methodologies',
                    'cloud architecture',
                    'API gateways',
                    'service-oriented architecture',
                    'event-driven architecture',
                    'continuous deployment'
                ]

                cloud_analyst_keywords = [
                    'cloud infrastructure management',
                    'firewalls',
                    'intrusion detection systems',
                    'network administration',
                    'load balancing',
                    'Linux/Unix administration',
                    'Terraform',
                    'cloud storage solutions',
                    'serverless architecture',
                    'cloud automation',
                    'cloud compliance',
                    'cloud networking'
                ]

                network_analyst_keywords = [
                    'TCP/IP networking',
                    'routing protocols',
                    'network security',
                    'troubleshooting',
                    'software-defined networking',
                    'wireless networking',
                    'network performance optimization',
                    'network capacity planning',
                    'VPN technologies',
                    'firewall configuration',
                    'network virtualization',
                    'intrusion detection/prevention systems',
                    'load balancing',
                    'packet analysis',
                    'network segmentation'
                ]

                cyber_security_analyst_keywords = [
                    'cyber threats',
                    'security risk assessment',
                    'penetration testing',
                    'incident response',
                    'identity and access management',
                    'compliance frameworks',
                    'threat intelligence analysis',
                    'security architecture design',
                    'security information and event management (SIEM)',
                    'endpoint security solutions',
                    'web application security',
                    'cloud security architecture',
                    'vulnerability management',
                    'security awareness training',
                    'security operations center (SOC)'
                ]

                hr_keywords = [
                    'human resource management',
                    'talent management',
                    'employee relations',
                    'performance management',
                    'compensation and benefits',
                    'HRIS',
                    'recruitment',
                    'onboarding',
                    'employee engagement',
                    'talent acquisition strategies',
                    'workforce planning',
                    'organizational development',
                    'employee training and development',
                    'HR metrics and analytics',
                    'diversity and inclusion'
                ]

                quality_assurance_keywords = [
                    'test planning',
                    'test case design',
                    'test automation',
                    'defect tracking',
                    'performance testing',
                    'agile methodologies',
                    'exploratory testing',
                    'security testing',
                    'usability testing',
                    'test-driven development',
                    'continuous testing',
                    'risk-based testing',
                    'test management tools',
                    'API testing',
                    'end-to-end testing'
                ]

                software_tester_keywords = [
                        'tester',
                        'testing',
                        'test automation',
                        'manual testing',
                        'integration testing',
                        'unit testing',
                        'CI/CD',
                        'agile methodologies',
                        'load testing',
                        'stress testing',
                        'black box testing',
                        'white box testing',
                        'regression testing',
                        'user acceptance testing',
                        'performance tuning',
                        'Selenium',
                        'BBD (Behavior Driven Development)',
                        'Playwright',
                        'Jenkins',
                        'Locust',
                        'JMeter',
                        'VAPT testing (Vulnerability Assessment and Penetration Testing)',
                        'DB Testing (Database Testing)',
                        'Docker',
                        'Git',
                        'Bitbucket',
                        'Cucumber',
                        'Testim',
                        'TestRail',
                        'Mobile Automation',
                        'OWASP Zap',
                        'IoT testing (Internet of Things testing)',
                        'AWS',
                        'pandas',
                        'TestNG',
                        'pytest'
                    ]


                ### Skill Recommendations Starts                
                recommended_skills = []
                reco_field = ''
                rec_course = ''

                ### condition starts to check skills from keywords and predict field
                for input in resume_data['skills']:
                    
                    
                    # Fashion Designer
                    if input.lower() in fashion_designer_keywords:
                        reco_field = 'Fashion Designer'
                        st.success("Our analysis says you are looking for Fashion Designer Jobs.")
                        recommended_skills =[
                            'MODARIS', 'ADOBE ILLUSTRATOR', 'MS OFFICE', 'MERCHANDISING', 'INDUSTRIAL ENGINEER', 
                            'QUALITY', 'creativity', 'fashion sketching', 'fabrics and textiles', 
                            'sewing and garment construction', 'color theory', 'trend awareness', 
                            'attention to detail', 'communication skills', 'business acumen', 
                            'adaptability', 'resilience'
                        ]
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='Fashion Designer skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(fashion_technology_courses)
                        break

                    
                    
                     # Cloud Analyst
                    elif input.lower() in cloud_analyst_keywords:
                        reco_field = 'Cloud Computing'
                        st.success("Our analysis says you are looking for Cloud Computing Jobs.")
                        recommended_skills = ['cloud computing', 'AWS', 'Azure', 'Google Cloud Platform', 'serverless computing', 'containerization', 'cloud security', 'cloud migration', 'cloud monitoring', 'cloud architecture', 'cloud cost optimization', 'PaaS', 'IaaS', 'SaaS', 'hybrid cloud', 'multi-cloud', 'cloud-native development', 'CI/CD for cloud', 'cloud networking']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='cloud_analyst_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(cloud_analyst_courses)
                        break
                
                    # Data Analyst
                    elif input.lower() in data_analyst_keywords:
                        reco_field = 'Data Science'
                        st.success("Our analysis says you are looking for Data Science Jobs.")
                        recommended_skills = ['data visualization', 'ETL', 'data cleaning', 'statistical analysis', 'business intelligence', 'SQL', 'data mining', 'predictive modeling', 'time series analysis', 'machine learning', 'natural language processing', 'big data technologies', 'data warehousing', 'dashboard development', 'reporting tools']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='data_analyst_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(data_analyst_courses)
                        break

                    # Database Administrator
                    elif input.lower() in database_administrator_keywords:
                        reco_field = 'Database Administration'
                        st.success("Our analysis says you are looking for Database Administration Jobs.")
                        recommended_skills = ['database management systems', 'database modeling', 'performance tuning', 'backup and recovery', 'database security', 'cloud-based databases', 'query optimization', 'database replication', 'disaster recovery planning', 'database migrations', 'data encryption', 'data integrity', 'data archival', 'distributed databases', 'database clustering']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='database_administrator_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(database_administrator_courses)
                        break

                    # DevOps Engineer
                    elif input.lower() in devops_engineer_keywords:
                        reco_field = 'DevOps Engineering'
                        st.success("Our analysis says you are looking for DevOps Engineering Jobs.")
                        recommended_skills = ['CI/CD', 'automation scripting', 'containerization', 'Docker', 'Kubernetes', 'cloud platform', 'continuous monitoring', 'log management', 'release management', 'infrastructure scaling', 'security automation', 'configuration drift detection', 'incident response automation', 'service discovery', 'immutable infrastructure']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='devops_engineer_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(devops_engineer_courses)
                        break
                         # Backend Developer
                    elif input.lower() in backend_developer_keywords:
                        reco_field = 'Backend Development'
                        st.success("Our analysis says you are looking for Backend Development Jobs.")
                        recommended_skills = ['backend developer', 'server', 'API', 'database', 'RESTful', 'Microservices', 'ORM', 'GraphQL', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud Platform', 'authentication', 'authorization', 'web security', 'performance optimization', 'cloud-native development', 'message brokers', 'serverless computing']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='backend_developer_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(backend_development_courses)
                        break

                    # Business Analyst
                    elif input.lower() in business_analyst_keywords:
                        reco_field = 'Business Analysis'
                        st.success("Our analysis says you are looking for Business Analysis Jobs.")
                        recommended_skills = ['requirements gathering', 'process modeling', 'data analysis', 'business intelligence', 'stakeholder management', 'problem-solving', 'project management', 'change management', 'business process reengineering', 'data-driven decision-making', 'business case development', 'user acceptance testing', 'root cause analysis', 'customer journey mapping', 'competitor analysis']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='business_analyst_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(business_analyst_courses)
                        break
                        
                    # Full Stack Developer
                    elif input.lower() in full_stack_developer_keywords:
                        reco_field = 'Full Stack Development'
                        st.success("Our analysis says you are looking for Full Stack Development Jobs.")
                        recommended_skills = ['full stack developer', 'web development', 'backend development', 'frontend development', 'testing', 'Git', 'CI/CD', 'containerization', 'DevOps', 'agile methodologies', 'microservices', 'database management', 'cloud platforms', 'authentication', 'authorization', 'web security', 'responsive design', 'cross-browser compatibility', 'UI/UX design']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='full_stack_developer_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(full_stack_developer_courses)
                        break


                    # Network Analyst
                    elif input.lower() in network_analyst_keywords:
                        reco_field = 'Network Analysis'
                        st.success("Our analysis says you are looking for Network Analysis Jobs.")
                        recommended_skills = ['networking', 'TCP/IP', 'routing protocols', 'network security', 'firewalls', 'VPN', 'wireless networks', 'LAN', 'WAN', 'network monitoring', 'network troubleshooting', 'packet analysis', 'DNS', 'DHCP', 'load balancing', 'SD-WAN', 'network performance optimization', 'network automation', 'software-defined networking']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='network_analyst_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(networking_analyst_courses)
                        break

                    # Cyber Security Analyst
                    elif input.lower() in cyber_security_analyst_keywords:
                        reco_field = 'Cybersecurity'
                        st.success("Our analysis says you are looking for Cybersecurity Jobs.")
                        recommended_skills = ['cybersecurity', 'network security', 'security operations', 'incident response', 'threat intelligence', 'vulnerability assessment', 'penetration testing', 'security monitoring', 'security awareness training', 'security risk management', 'security compliance', 'identity and access management', 'security architecture', 'data encryption', 'cloud security', 'mobile security', 'endpoint security', 'web application security', 'security audits']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='cyber_security_analyst_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(cyber_security_analyst_courses)
                        break

                    # HR
                    elif input.lower() in hr_keywords:
                        reco_field = 'Human Resources'
                        st.success("Our analysis says you are looking for Human Resources Jobs.")
                        recommended_skills = ['recruitment', 'employee relations', 'performance management', 'compensation and benefits', 'training and development', 'HR policies and procedures', 'talent management', 'workforce planning', 'HR analytics', 'employee engagement', 'diversity and inclusion', 'HRIS', 'labor laws and regulations', 'organizational development', 'succession planning', 'change management', 'HR technology', 'onboarding', 'offboarding', 'workplace health and safety']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='hr_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(hr_courses)
                        break

                    # Quality Assurance
                    elif input.lower() in quality_assurance_keywords:
                        reco_field = 'Quality Assurance'
                        st.success("Our analysis says you are looking for Quality Assurance Jobs.")
                        recommended_skills = ['quality assurance', 'software testing', 'test planning', 'test automation', 'test case design', 'defect tracking', 'regression testing', 'user acceptance testing', 'performance testing', 'load testing', 'security testing', 'CI/CD', 'agile methodologies', 'test management tools', 'test documentation', 'exploratory testing', 'continuous testing', 'test-driven development', 'code reviews', 'bug triage']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='quality_assurance_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(quality_assurance_courses)
                        break

                    # Software Tester
                    elif input.lower() in software_tester_keywords:
                        reco_field = 'Software Testing'
                        st.success("Our analysis says you are looking for Software Testing Jobs.")
                        recommended_skills = ['software testing', 'test planning', 'test automation', 'test case design', 'defect tracking', 'regression testing', 'user acceptance testing', 'performance testing', 'load testing', 'security testing', 'CI/CD', 'agile methodologies', 'test management tools', 'test documentation', 'exploratory testing', 'continuous testing', 'test-driven development', 'code reviews', 'bug triage']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills,
                                                    key='software_tester_recommended_skills')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost the chances of getting a job</h5>''', unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(software_tester_courses)
                        break



                ## Resume Scorer & Resume Writing Tips
                st.subheader("Resume Tips & Ideas")
                resume_score = 0
                
                ### Predicting Whether these key points are added to the resume
                if 'Objective' or 'Summary' in resume_text:
                    resume_score = resume_score+6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h4>''',unsafe_allow_html=True)                
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if 'Education' or 'School' or 'College'  in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)

                if 'EXPERIENCE' in resume_text:
                    resume_score = resume_score + 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                elif 'Experience' in resume_text:
                    resume_score = resume_score + 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

                if 'INTERNSHIPS'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'INTERNSHIP'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'Internships'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'Internship'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

                if 'SKILLS'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'SKILL'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'Skills'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'Skill'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)

                if 'HOBBIES' in resume_text:
                    resume_score = resume_score + 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
                elif 'Hobbies' in resume_text:
                    resume_score = resume_score + 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if 'INTERESTS'in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
                elif 'Interests'in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Interest. It will show your interest other that job.</h4>''',unsafe_allow_html=True)

                if 'ACHIEVEMENTS' in resume_text:
                    resume_score = resume_score + 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                elif 'Achievements' in resume_text:
                    resume_score = resume_score + 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                if 'CERTIFICATIONS' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                elif 'Certifications' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                elif 'Certification' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

                if 'PROJECTS' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'PROJECT' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'Projects' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'Project' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader("Resume Score")
                
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )

                ### Score Bar
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)

                ### Score
                st.success('ATS RESUME Score: ' + str(score)+'**')
                st.warning("This score is calculated based on the content that you have in your Resume")

                # print(str(sec_token), str(ip_add), (host_name), (dev_user), (os_name_ver), (latlong), (city), (state), (country), (act_name), (act_mail), (act_mob), resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)


                ### Getting Current Date and Time
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)


                ## Calling insert_data to add all the data into user_data                
                insert_data(str(sec_token), str(ip_add), (host_name), (dev_user), (os_name_ver), (latlong), (city), (state), (country), (act_name), (act_mail), (act_mob), resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)

                ## Recommending Resume Writing Video
                st.header("Videos for Resume Writing Tips")
                resume_vid = random.choice(resume_videos)
                st.video(resume_vid)

                ## Recommending Interview Preparation Video
                st.header("Videos for Interview Tips")
                interview_vid = random.choice(interview_videos)
                st.video(interview_vid)
            else:
                st.error('Something went wrong..')                


    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':   
        
        # timestamp 
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date+'_'+cur_time)

        # Feedback Form
        with st.form("my_form"):
            st.write("Feedback form")            
            feed_name = st.text_input('Name')
            feed_email = st.text_input('Email')
            feed_score = st.slider('Rate Us From 1 - 5', 1, 5)
            comments = st.text_input('Comments')
            Timestamp = timestamp        
            submitted = st.form_submit_button("Submit")
            if submitted:
                ## Calling insertf_data to add dat into user feedback
                insertf_data(feed_name,feed_email,feed_score,comments,Timestamp)    
                ## Success Message 
                st.success("Thanks! Your Feedback was recorded.") 
               


        # query to fetch data from user feedback table
        query = 'select * from user_feedback'        
        plotfeed_data = pd.read_sql(query, connection)                      
    


    ###### CODE FOR ADMIN SIDE (ADMIN) ######
    else:
        st.success('Welcome to Admin Side')

        #  Admin Login
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')

        if st.button('Login'):
            
            ## Credentials 
            if ad_user == 'admin' and ad_password == 'admin':
                
                ### Fetch miscellaneous data from user_data(table) and convert it into dataframe
                cursor.execute('''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8), convert(User_level using utf8), city, state, country from user_data''')
                datanalys = cursor.fetchall()
                plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score', 'Predicted_Field', 'User_Level', 'City', 'State', 'Country'])
                
                ### Total Users Count with a Welcome Message
                values = plot_data.Idt.count()
                st.success("Welcome  ! Total %d " % values + " User's Have Used Our Tool : )")                
                
                ### Fetch user data from user_data(table) and convert it into dataframe
                cursor.execute('''SELECT ID, sec_token, ip_add, Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name, convert(User_level using utf8), convert(Actual_skills using utf8), convert(Recommended_skills using utf8), convert(Recommended_courses using utf8), city, state, country, latlong, os_name_ver, host_name, dev_user from user_data''')
                data = cursor.fetchall()                

                st.header("User's Data")
                df = pd.DataFrame(data, columns=['ID', 'Token', 'IP Address', 'Timestamp',
                                                 'Predicted Name', 'Predicted Mail', 'Resume Score', 'Total Page',  'File Name',   
                                                 'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course',
                                                 'City', 'State', 'Country', 'Lat Long', 'Server OS', 'Server Name', 'Server User',])
                
                ### Viewing the dataframe
                st.dataframe(df)
                
                ### Downloading Report of user_data in csv file
                st.markdown(get_csv_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)

                ### Fetch feedback data from user_feedback(table) and convert it into dataframe
                cursor.execute('''SELECT * from user_feedback''')
                data = cursor.fetchall()

                st.header("User's Feedback Data")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Feedback Score', 'Comments', 'Timestamp'])
                st.dataframe(df)

                ### query to fetch data from user_feedback(table)
                query = 'select * from user_feedback'
                plotfeed_data = pd.read_sql(query, connection)                        

                ### Analyzing All the Data's in pie charts

                # fetching feed_score from the query and getting the unique values and total value count 
                labels = plotfeed_data.feed_score.unique()
                values = plotfeed_data.feed_score.value_counts()
                
                # Pie chart for user ratings
                st.subheader("User Rating's")
                fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5 🤗", color_discrete_sequence=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig)

                # fetching Predicted_Field from the query and getting the unique values and total value count                 
                labels = plot_data.Predicted_Field.unique()
                values = plot_data.Predicted_Field.value_counts()

                # Pie chart for predicted field recommendations
                st.subheader("Pie-Chart for Predicted Field Recommendation")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
                st.plotly_chart(fig)



                # fetching IP_add from the query and getting the unique values and total value count 
                labels = plot_data.IP_add.unique()
                values = plot_data.IP_add.value_counts()

                # Pie chart for Users
                st.subheader("Pie-Chart for Users App Used Count")
                fig = px.pie(df, values=values, names=labels, title='Usage Based On IP Address', color_discrete_sequence=px.colors.sequential.matter_r)
                st.plotly_chart(fig)

                # fetching City from the query and getting the unique values and total value count 
                labels = plot_data.City.unique()
                values = plot_data.City.value_counts()

                # Pie chart for City
                st.subheader("Pie-Chart for City")
                fig = px.pie(df, values=values, names=labels, title='Usage Based On City', color_discrete_sequence=px.colors.sequential.Jet)
                st.plotly_chart(fig)

                # fetching State from the query and getting the unique values and total value count 
                labels = plot_data.State.unique()
                values = plot_data.State.value_counts()

                # Pie chart for State
                st.subheader("Pie-Chart for State")
                fig = px.pie(df, values=values, names=labels, title='Usage Based on State', color_discrete_sequence=px.colors.sequential.PuBu_r)
                st.plotly_chart(fig)

                # fetching Country from the query and getting the unique values and total value count 
                labels = plot_data.Country.unique()
                values = plot_data.Country.value_counts()

                # Pie chart for Country
                st.subheader("Pie-Chart for Country")
                fig = px.pie(df, values=values, names=labels, title='Usage Based on Country', color_discrete_sequence=px.colors.sequential.Purpor_r)
                st.plotly_chart(fig)

            ## For Wrong Credentials
            else:
                st.error("Wrong ID & Password Provided")
                

# Calling the main (run()) function to make the whole process run
run()
