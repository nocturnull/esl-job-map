SUBJECT_BASE_SCHEME = """{title} via ESLJobMap.com"""
AUTHENTICATED_USER_BASE_SCHEME = """{recruiter_name},

{visa_status}I am a national of and have a passport from {applicant_country}. I am applying for the below job:

{job_post_title}
{exclusive_job_post_info}
Schedule: {job_post_schedule}
Class Type: {job_post_class_type}
Other Requirements: {job_post_other_requirements}
Address: {job_post_address}

Please find attached my photo and resume. Thank you for considering my application.

Regards,

{applicant_full_name}
{applicant_email}
{applicant_contact_number}"""
ANONYMOUS_USER_BASE_SCHEME = "{recruiter_name},"

FULL_TIME_EXCLUSIVE_SCHEME = """Salary: {job_post_salary}
Benefits: {job_post_benefits}"""

PART_TIME_EXCLUSIVE_SCHEME = """Pay Rate: {job_post_pay_rate}"""
