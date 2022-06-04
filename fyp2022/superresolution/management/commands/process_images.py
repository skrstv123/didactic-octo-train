from django.core.management.base import BaseCommand
from superresolution.models import Job
from django.core import management
from PIL import Image
from superresolution.management.emailer import send_email
import numpy as np

class Command(BaseCommand):
    help = """
        processes job and email result to customer.
        processes all jobs that are pending or processed.
        processs oldest job first.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        """
        proccess oldest pending job first.
        """
        def get_op_file_name_path(job):
            return f'output_files/OP_{job.input_file}', f"OP_{job.input_file}"

        self.get_op_path_name = get_op_file_name_path

        def printstats(job_to_process):
            print(f"Job {job_to_process.id} status:",
            job_to_process.title,
            job_to_process.status,
            job_to_process.input_file, sep="\t")

        jobs = Job.objects.filter(status__in = ['pending', 'processed']).order_by("-added_at")
        if jobs.exists():
            job_to_process = jobs.first()
            printstats(job_to_process)
            result_dic = self.process_job(job_to_process)
            if 'error' not in result_dic:
                try:
                    if job_to_process.status != "processed":
                        img = Image.fromarray(np.asarray(result_dic['super_image']))
                        path, name = self.get_op_path_name(job_to_process)
                        img.save(path)
                        self.stdout.write(self.style.SUCCESS(f"Successfully processed job {job_to_process.id}."))
                        job_to_process.status = "processed"
                        job_to_process.save()
                    try:
                        self.send_mail(job_to_process, result_dic)
                        self.stdout.write(self.style.SUCCESS(f"Successfully sent email to customer."))
                        job_to_process.status = "sent"
                        job_to_process.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to send email to customer."))
                        self.stdout.write(self.style.ERROR(f"{e}"))
                        job_to_process.status = "processed"
                        job_to_process.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing job {job_to_process.id}."))
                    self.stdout.write(self.style.ERROR(f"{e}"))
                    job_to_process.status = "failed"
            printstats(job_to_process)
            
    def send_mail(self, job, result_dic):
        """
        send email to customer.
        """
        path, name = self.get_op_path_name(job)
        result_dic['file_name'] = name
        with open(path, "rb") as f:
            result_dic['file'] = f.read()
        result_dic['message'] = f"Your job {job.id} with title {job.title} has been processed!"
        result_dic['subject'] = f"Job {job.id} with title {job.title} has been processed!"
        result_dic['to'] = job.out_email
        send_email(result_dic)

    def process_job(self, job):
        """
        proccess job and email result to customer.
        """
        load_image = lambda path: np.asarray(Image.open(path))
        result_dic = {}
        def load_model():
            model = generator()
            model.load_weights("superresolution/management/commands/srganmodel.h5")
            self.srganmodel = model
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded model."))
        def get_path(job):
            return f'input_files/{job.input_file}'
        def get_output_path(job):
            return f'output_files/OP_{job.input_file}'

        img_array = load_image(get_path(job))
        if job.status == "processed":
            self.stdout.write(self.style.WARNING(f"Job {job.id} is already processed."))
            result = load_image(get_output_path(job))
        else:
            from superresolution.management.srgan import generator, resolve_single
            load_model()
            result = resolve_single(self.srganmodel, img_array)
    
        print("input image shape:",img_array.shape, "\noutput image shape:", result.shape)

        result_dic['input_image_shape'] = img_array.shape
        result_dic['super_image_shape'] = result.shape
        result_dic['super_image'] = result
        
        return result_dic
        
            