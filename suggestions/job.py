from flask import Flask, request

app = Flask(__name__,static_url_path='/static')

# Mock database function
def get_companies_by_job_role(job_role):
    # This is a mock function, replace it with actual database interaction logic
    if job_role.lower() == 'software engineer':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
        ]
    elif job_role.lower() == 'data scientist':
        return [
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Accenture', 'url': 'https://www.accenture.com/us-en/careers'},
            {'name': 'Deloitte', 'url': 'https://www2.deloitte.com/us/en/careers.html'},
            {'name': 'KPMG', 'url': 'https://home.kpmg/us/en/home/careers.html'},
            {'name': 'PwC', 'url': 'https://www.pwc.com/us/en/careers.html'},
            {'name': 'EY', 'url': 'https://www.ey.com/en_us/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
        ]
    elif job_role.lower() == 'data analyst':
        return [
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Accenture', 'url': 'https://www.accenture.com/us-en/careers'},
            {'name': 'Deloitte', 'url': 'https://www2.deloitte.com/us/en/careers.html'},
            {'name': 'KPMG', 'url': 'https://home.kpmg/us/en/home/careers.html'},
            {'name': 'PwC', 'url': 'https://www.pwc.com/us/en/careers.html'},
            {'name': 'EY', 'url': 'https://www.ey.com/en_us/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
        ]
    elif job_role.lower() == 'business analyst':
        return [
            {'name': 'McKinsey & Company', 'url': 'https://www.mckinsey.com/careers'},
            {'name': 'Bain & Company', 'url': 'https://www.bain.com/careers/'},
            {'name': 'Boston Consulting Group (BCG)', 'url': 'https://www.bcg.com/careers/'},
            {'name': 'Deloitte', 'url': 'https://www2.deloitte.com/us/en/careers.html'},
            {'name': 'KPMG', 'url': 'https://home.kpmg/us/en/home/careers.html'},
            {'name': 'PwC', 'url': 'https://www.pwc.com/us/en/careers.html'},
            {'name': 'EY', 'url': 'https://www.ey.com/en_us/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Accenture', 'url': 'https://www.accenture.com/us-en/careers'},
        ]
    elif job_role.lower() == 'data_analyst':
        return [
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Accenture', 'url': 'https://www.accenture.com/us-en/careers'},
            {'name': 'Deloitte', 'url': 'https://www2.deloitte.com/us/en/careers.html'},
            {'name': 'KPMG', 'url': 'https://home.kpmg/us/en/home/careers.html'},
            {'name': 'PwC', 'url': 'https://www.pwc.com/us/en/careers.html'},
            {'name': 'EY', 'url': 'https://www.ey.com/en_us/careers'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
        ]
    elif job_role.lower() == 'database_administrator':
        return [
            {'name': 'Oracle', 'url': 'https://www.oracle.com/corporate/careers/'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
        ]
    elif job_role.lower() == 'devops_engineer':
        return [
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
        ]
    elif job_role.lower() == 'backend_development':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'business_analyst':
        return [
            {'name': 'McKinsey & Company', 'url': 'https://www.mckinsey.com/careers'},
            {'name': 'Bain & Company', 'url': 'https://www.bain.com/careers/'},
            {'name': 'Boston Consulting Group (BCG)', 'url': 'https://www.bcg.com/careers/'},
            {'name': 'Deloitte', 'url': 'https://www2.deloitte.com/us/en/careers.html'},
            {'name': 'KPMG', 'url': 'https://home.kpmg/us/en/home/careers.html'},
            {'name': 'PwC', 'url': 'https://www.pwc.com/us/en/careers.html'},
            {'name': 'EY', 'url': 'https://www.ey.com/en_us/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Accenture', 'url': 'https://www.accenture.com/us-en/careers'},
        ]
    elif job_role.lower() == 'fashion_technology':
        return [
            {'name': 'LVMH', 'url': 'https://www.lvmh.com/talents/our-job-offers/'},
            {'name': 'Kering', 'url': 'https://www.kering.com/en/talent/job-offers/'},
            {'name': 'Nike', 'url': 'https://jobs.nike.com/'},
            {'name': 'Adidas', 'url': 'https://careers.adidas-group.com/'},
            {'name': 'Gap Inc.', 'url': 'https://jobs.gapinc.com/'},
            {'name': 'Zara', 'url': 'https://www.inditexcareers.com/portalweb/en/web/ofertas-empleo'},
            {'name': 'H&M', 'url': 'https://career.hm.com/content/hmcareer/en_us.html'},
            {'name': 'Under Armour', 'url': 'https://careers.underarmour.com/'},
            {'name': 'Levi Strauss & Co.', 'url': 'https://www.levistrauss.com/careers/'},
            {'name': 'PVH Corp.', 'url': 'https://www.pvh.com/jobs'},
        ]
    elif job_role.lower() == 'full_stack_developer':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'cloud_analyst':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'Oracle', 'url': 'https://www.oracle.com/corporate/careers/'},
            {'name': 'Salesforce', 'url': 'https://www.salesforce.com/company/careers/'},
            {'name': 'VMware', 'url': 'https://careers.vmware.com/main/'},
            {'name': 'Alibaba Cloud', 'url': 'https://careers.alibabacloud.com/'},
            {'name': 'Tencent Cloud', 'url': 'https://careers.tencent.com/global'},
            {'name': 'Rackspace Technology', 'url': 'https://www.rackspace.com/careers'},
        ]
    elif job_role.lower() == 'cyber_security_analyst':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'hr':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'quality_assurance':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'networking_analyst':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    elif job_role.lower() == 'software_tester':
        return [
            {'name': 'Google', 'url': 'https://www.google.com/careers'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/careers'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
            {'name': 'Microsoft', 'url': 'https://careers.microsoft.com/'},
            {'name': 'Apple', 'url': 'https://www.apple.com/jobs/us/'},
            {'name': 'Netflix', 'url': 'https://jobs.netflix.com/jobs'},
            {'name': 'Adobe', 'url': 'https://www.adobe.com/careers.html'},
            {'name': 'Intel', 'url': 'https://jobs.intel.com/'},
            {'name': 'Uber', 'url': 'https://www.uber.com/us/en/careers/'},
            {'name': 'Tesla', 'url': 'https://www.tesla.com/careers'},
            {'name': 'IBM', 'url': 'https://www.ibm.com/employment'},
            {'name': 'LinkedIn', 'url': 'https://careers.linkedin.com/'},
            {'name': 'Twitter', 'url': 'https://careers.twitter.com/en.html'},
            {'name': 'Amazon', 'url': 'https://www.amazon.jobs'},
        ]
    else:
        return []

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Search</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-image: url(/static/home.jpg.jpg); /* Background image for homepage */
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                max-width: 400px;
                background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }

            input[type="text"], button {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                box-sizing: border-box;
            }

            button {
                background-color: #007bff;
                color: #fff;
                border: none;
                cursor: pointer;
                border-radius: 3px;
            }

            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="text-align: center; color: #333;">Enter Job Role:</h1>
            <form action="/search" method="post">
                <input type="text" name="job_role" placeholder="Enter job role" style="margin-bottom: 10px;">
                <button type="submit">Search</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/search', methods=['POST'])
def search():
    job_role = request.form['job_role']
    companies = get_companies_by_job_role(job_role)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Search Results</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-image: url('/static/result.jpg.png'); /* Background image for search results page */
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                max-width: 600px;
                background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}

            ul {{
                list-style-type: none;
                padding: 0;
            }}

            ul li {{
                margin-bottom: 10px;
            }}

            a {{
                text-decoration: none;
                color: #007bff;
            }}

            a:hover {{
                text-decoration: underline;
                color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="text-align: center; color: #333;">Companies Hiring for {job_role}</h1>
            <ul>
                {''.join([f"<li><a href='{company['url']}' style='color: #333;'>{company['name']}</a></li>" for company in companies])}
            </ul>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)