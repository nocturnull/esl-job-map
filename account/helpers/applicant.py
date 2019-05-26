# account/helpers/applicant.py

from ..models import Resume, Photo

from cloud.file_manager import FileManager


class ProfileHelper:
    """Profile model helper class"""

    @staticmethod
    def save_resume(applicant, resume_file):
        """
        Attempt to upload a resume file.

        :param applicant:
        :param resume_file:
        :return:
        """
        if resume_file:
            file_manager = FileManager()
            new_resume = Resume.create_resume(filename=resume_file.name)
            file_manager.upload_file(new_resume.storage_path, resume_file)
            applicant.resume = new_resume
            applicant.save()

    @staticmethod
    def save_photo(applicant, photo_file):
        """
        Attempt to upload a photo file.

        :param applicant:
        :param photo_file:
        :return:
        """
        if photo_file:
            file_manager = FileManager()
            new_photo = Photo.create_photo(filename=photo_file.name)
            file_manager.upload_file(new_photo.storage_path, photo_file)
            applicant.photo = new_photo
            applicant.save()
