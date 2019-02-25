SUBJECT_BASE_SCHEME = """Job: {title} has expired"""
BODY_BASE_SCHEME = """<h2>Hello {contact_name},</h2>
<h4>
The following job has expired:<br/>
아래 포스팅 기간이 만료되었습니다:
</h4>

<div>
<strong>{title}</strong><br/>
{exclusive_info_section}
<strong>Schedule</strong>: {schedule}<br/>
<strong>Class Type</strong>: {class_type}<br/>
<strong>Other Requirements</strong>: {other_requirements}<br/>
<strong>Address</strong>: {address}<br/>
</div>
<br/>
{applicants_notice_section}
<br/>
Regards,
<br/>
ESL Job Map"""

FULL_TIME_EXCLUSIVE_SCHEME = """
<strong>Salary</strong>: {salary}<br/>
<strong>Benefits</strong>: {benefits}<br/>"""

PART_TIME_EXCLUSIVE_SCHEME = """<strong>Pay Rate</strong>: {pay_rate}<br/>"""

HAS_APPLICANTS_SCHEME = """
<div>
Looks like you got <a href="{applicants_job_post_url}" target="_blank">{num_applicants} applicants.</a> If you are still looking for applicants, please repost the job <a href="{repost_job_post_url}" target="_blank">HERE</a>.<br/>
포스팅 기간 동안 총 <a href="{applicants_job_post_url}" target="_blank">{num_applicants} 명의</a> 지원자를 받으신 걸로 집계됩니다. 아직 지원자를 찾고 계시다면 <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 해주시기 바랍니다.<br/>
</div>
"""

NO_APPLICANTS_SCHEME = """
<div>
Looks like you didn’t get any applicants. You can <a href="{repost_job_post_url}" target="_blank">repost</a> the job, or consider writing it differently and post it as a <a href="{create_job_post_url}" target="_blank">new job</a>.<br/>
아직 지원자를 받지 않으신 걸로 보입니다. <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 하시거나, <a href="{create_job_post_url}" target="_blank">여기를 클릭하여 새롭게 포스팅</a>을 올리실 수 있습니다.<br/> 
</div>
"""