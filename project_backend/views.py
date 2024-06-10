from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializer import FileUploadSerializer
import os
from django.conf import settings
from rest_framework import status
from CodeFolder.main import Get_score
from CodeFolder.OCR import image_to_text


def first_page(request):
    return HttpResponse('you have successfully deployed your app')

@api_view(['GET', 'POST'])
def ExtendedDataprocess(request):
    if request.method == 'GET':
        return Response({'msg': 'Your GET request was successful'})

    if request.method == 'POST':
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            image = serializer.validated_data.get('image', None)
            solutionimage = serializer.validated_data.get('solutionimage', None)
            solution = serializer.validated_data.get('solution', None)
            answer = serializer.validated_data.get('answer', None)

            if solutionimage:
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                file_path = os.path.join(destination_dir, solutionimage.name)

                with open(file_path, 'wb+') as destination:
                    for chunk in solutionimage.chunks():
                        destination.write(chunk)

                if file_path.endswith(('txt', 'png', 'jpg', 'jpeg')):
                    if file_path.endswith('txt'):
                        with open(file_path, 'r') as f:
                            solution = f.read()
                    else:
                        solution = image_to_text(file_path)

            if image:
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                file_path = os.path.join(destination_dir, image.name)

                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                if file_path.endswith(('txt', 'png', 'jpg', 'jpeg')):
                    if file_path.endswith('txt'):
                        with open(file_path, 'r') as f:
                            answer = f.read()
                    else:
                        answer = image_to_text(file_path)

            output = Get_score(solution, answer)

            return Response({'output': output, 'solution': solution, 'answer': answer}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
