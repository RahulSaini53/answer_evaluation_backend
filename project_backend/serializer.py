from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    image = serializers.FileField(required=False,allow_empty_file=True)
    solutionimage = serializers.FileField(required=False,allow_empty_file=True)
    solution = serializers.CharField(required=False,allow_blank=True)
    answer = serializers.CharField(required=False,allow_blank=True)

    def validate(self, data):
        image = data.get('image')
        answer = data.get('answer')
        if not image and not answer:
            raise serializers.ValidationError("Either 'image' or 'answer' must be provided.")
        
        return data