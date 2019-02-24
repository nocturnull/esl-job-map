SUBJECT_BASE_SCHEME = """Job: {title} has expired"""
BODY_BASE_SCHEME = """<h2>Hello {contact_name}</h2>,
<h4>
The following job has expired:<br/>
아래 포스팅 기간이 만료되었습니다:
</h4>

<div>
<strong>{title}</strong>
{exclusive_info_section}
<strong>Schedule</strong>: {schedule}
<strong>Class Type</strong>: {class_type}
<strong>Other Requirements</strong>: {other_requirements}
<strong>Address</strong>: {address}
</div>

{applicants_notice_section}

Regards,

ESL Job Map"""

FULL_TIME_EXCLUSIVE_SCHEME = """Salary: {salary}
Benefits: {benefits}"""

PART_TIME_EXCLUSIVE_SCHEME = """Pay Rate: {pay_rate}"""

HAS_APPLICANTS_SCHEME = """
<div>
Looks like you got <a href="{applicants_job_post_url}" target="_blank">{num_applicants}</a><br/>
If you are still looking for applicants, please repost the job <a href="{repost_job_post_url}" target="_blank">HERE</a>.<br/>
포스팅 기간 동안 총 <a href="{applicants_job_post_url}" target="_blank">{num_applicants}</a>명의 지원자를 받으신 걸로 집계됩니다.<br/>
아직 지원자를 찾고 계시다면 <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 해주시기 바랍니다.
</div>
"""

NO_APPLICANTS_SCHEME = """
<div>
Looks like you didn’t get any applicants. You can <a href="{repost_job_post_url}" target="_blank">repost</a> the job,<br/>
or consider writing it differently and post it as a <a href="{create_job_post_url}" target="_blank">new job</a>.
아직 지원자를 받지 않으신 걸로 보입니다. <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 하시거나,<br/>
<a href="{create_job_post_url}" target="_blank">여기를 클릭하여 새롭게 포스팅</a>을 올리실 수 있습니다. 
</div>
"""