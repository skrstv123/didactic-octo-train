from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'job_type', 'status', 'added_at', "out_email"]
        read_only_fields = ['id', 'status', 'added_at', 'job_submitted_by']

    def validate(self, data):
        data['job_submitted_by'] = self.context['request'].user
        assert 'input_file' in self.context['request'].data
        if data.get('out_email', '').strip() == '':
            data['out_email'] = self.context['request'].user.email
        return super().validate(data)
