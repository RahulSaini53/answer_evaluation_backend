from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import FileUploadSerializer
import time
import os
from django.conf import settings
from rest_framework import status
from CodeFolder.main import Get_score
from CodeFolder.OCR import image_to_text

    
@api_view(['GET', 'POST'])
def ExtendedDataprocess(request):
    if(request.method == 'GET'):
        return Response({'msg':'your get request was successful'})
    
    if(request.method == 'POST'):
       
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
           
            image = serializer.validated_data.get('image', None)
            solutionimage = serializer.validated_data.get('solutionimage', None)
            solution = serializer.validated_data.get('solution', None)
            answer = serializer.validated_data.get('answer',None)
        

            if(solutionimage):
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Define your desired destination directory
            
                    # Process uploaded files
            
                file_path = os.path.join(destination_dir, solutionimage.name)
               
                
                # Save the file to the destination directory
                with open(file_path, 'wb+') as destination:
                    for chunk in solutionimage.chunks():
                        destination.write(chunk)
                
                if(file_path[-3:]=='txt'):
                  f=open(file_path,'r+')
                  solution=f.read()

                elif(file_path[-3:]=='png' or file_path[-3:]=='jpg' or file_path[-4:]=='jpeg'):
                    solution=image_to_text(file_path)
                   
           
            if(image):
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Define your desired destination directory
            
                    # Process uploaded files
            
                file_path = os.path.join(destination_dir, image.name)
           
                
                # Save the file to the destination directory
                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                
                if(file_path[-3:]=='txt'):
                  f=open(file_path,'r+')
                  answer=f.read()
                 
                elif(file_path[-3:]=='png' or file_path[-3:]=='jpg' or file_path[-4:]=='jpeg'):
                    answer=image_to_text(file_path)
           

            output=Get_score(solution,answer)
            
            return Response({'output':output,'solution':solution,'answer':answer}, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)