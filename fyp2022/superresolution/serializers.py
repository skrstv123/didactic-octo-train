from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['status', 'added_at', 'job_submitted_by', 'input_file',]

    def validate(self, data):
        data['job_submitted_by'] = self.context['request'].user
        assert 'input_file' in self.context['request'].data
        return super().validate(data)
