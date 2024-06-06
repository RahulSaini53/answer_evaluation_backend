from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import FileUploadSerializer
from CodeFolder import process_data
import time
import os
from django.conf import settings
from rest_framework import status
from CodeFolder.main import Get_score
from CodeFolder.OCR import image_to_text


@api_view(['GET', 'POST'])
def dataprocess(request):
    if request.method == 'GET':
        num=request.data
        print(num)
        return Response({'msg':'your get request was successful'})
    if request.method == 'POST':
        strings=request.data
        # x=process_data.factorial(num)
        print(strings)
        str1 = strings.getlist('solution')[0]
        str2 = strings.getlist('answer')[0]
        print(str1,str2)
        output=process_data.compare_data(str1,str2)
        print(output)
        time.sleep(5)
        return Response(output)
    
    
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
            # print(solutionimage,image)
            print('solutionimage:',solutionimage)

            if(solutionimage):
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Define your desired destination directory
            
                    # Process uploaded files
            
                file_path = os.path.join(destination_dir, solutionimage.name)
                # print(solutionimage.name)
                
                # Save the file to the destination directory
                with open(file_path, 'wb+') as destination:
                    for chunk in solutionimage.chunks():
                        destination.write(chunk)
                
                if(file_path[-3:]=='txt'):
                  f=open(file_path,'r+')
                  solution=f.read()
                  print('solution text=',solution)
                  print()

                elif(file_path[-3:]=='png' or file_path[-3:]=='jpg' or file_path[-4:]=='jpeg'):
                    solution=image_to_text(file_path)
                    print('solution png text=',solution)
                    print()

           
            if(image):
                destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Define your desired destination directory
            
                    # Process uploaded files
            
                file_path = os.path.join(destination_dir, image.name)
                print(image.name)
                
                # Save the file to the destination directory
                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                
                if(file_path[-3:]=='txt'):
                  f=open(file_path,'r+')
                  answer=f.read()
                  print('answer text=', answer)
                  print()
                elif(file_path[-3:]=='png' or file_path[-3:]=='jpg' or file_path[-4:]=='jpeg'):
                    answer=image_to_text(file_path)
                    print('answer png text=',answer)
                

            # print(answer,'\n',solution)
            output=Get_score(solution,answer)
            print(output)
            # time.sleep(2)
            return Response({'output':output,'solution':solution,'answer':answer}, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)