SUBJECT_BASE_SCHEME = """Job: {title} has expired"""
BODY_BASE_SCHEME = """<div>Hello {recruiter_name},<br/></div>
<br/>
<div>
The following job has expired:<br/>
아래 포스팅 기간이 만료되었습니다:
</div>
<br/>
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
<div>
If you no longer wish to receive job expired reminder emails, <a href="{email_opt_out_link}" target="_blank">click here</a><br/>
포스팅 만료 안내 메일을 그만 받고 싶으시면 <a href="{email_opt_out_link}" target="_blank">여기를 클릭</a> 하세요.
</div>
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
Looks like you got <a href="{applicants_job_post_url}" target="_blank">{num_applicants} applicants.</a> If you are still looking for applicants, please <a href="{repost_job_post_url}" target="_blank">repost the job here</a>.<br/>
포스팅 기간 동안 총 <a href="{applicants_job_post_url}" target="_blank">{num_applicants} 명의 지원자</a>를 받으신 걸로 집계됩니다. 아직 지원자를 찾고 계시다면 <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 해주시기 바랍니다.<br/>
</div>
"""

NO_APPLICANTS_SCHEME = """
<div>
Looks like you didn’t get any applicants. You can <a href="{repost_job_post_url}" target="_blank">repost</a> the job, or consider writing it differently and <a href="{create_job_post_url}" target="_blank">post it as a new job</a>.<br/>
아직 지원자를 받지 않으신 걸로 보입니다. <a href="{repost_job_post_url}" target="_blank">여기를 클릭하여 Repost</a> 하시거나, <a href="{create_job_post_url}" target="_blank">여기를 클릭하여 새롭게 포스팅</a>을 올리실 수 있습니다.<br/> 
</div>
"""