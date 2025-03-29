from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Loan
from .serializers import LoanSerializer

def first_api(request):
  return JsonResponse({'message': 'API is working!'})


@api_view(['GET', 'POST'])
def items_list(request):

    string_fields = ['borrower', 'co_borrower_name', 'region', 'state', 'category', 'loan_type', 'borrower_address', 'co_borrower_address']

    if request.method == 'GET':
        try:
            filters = request.query_params.dict()
            queryset = Loan.objects.all()

            valid_fields = [f.name for f in Loan._meta.get_fields()]
            for field, value in filters.items():
                if field in valid_fields and value not in [None, '']:
                    if field.endswith('__gt'):
                        queryset = queryset.filter(**{field: value})
                    elif field.endswith('__lt'):
                        queryset = queryset.filter(**{field: value})
                    elif field.endswith('__icontains'):
                        queryset = queryset.filter(**{field: value})
                    elif field in string_fields:
                        queryset = queryset.filter(**{f"{field}__icontains": value})
                    else:
                        queryset = queryset.filter(**{field: value})

            page = int(filters.get('page', 1))
            page_size = int(filters.get('page_size', 10))
            paginator = Paginator(queryset, page_size)

            try:
                loans = paginator.page(page)
            except PageNotAnInteger:
                loans = paginator.page(1)
            except EmptyPage:
                loans = paginator.page(paginator.num_pages)

            serializer = LoanSerializer(loans, many=True)
            return Response({
                'success': True,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'results': serializer.data
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        try:
            loan_no = request.data.get('loan_no')
            if Loan.objects.filter(loan_no=loan_no).exists():
                return Response(
                    {"error": "Loan with this loan_no already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = LoanSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Loan
from .serializers import LoanSerializer

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def loan_operations(request, loan_no):
    try:
        # Get the loan object or return 404
        loan = get_object_or_404(Loan, loan_no=loan_no)
        
        # Handle GET request (retrieve)
        if request.method == 'GET':
            serializer = LoanSerializer(loan)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        # Handle PUT/PATCH requests (update)
        elif request.method in ['PUT', 'PATCH']:
            serializer = LoanSerializer(
                loan, 
                data=request.data, 
                partial=request.method == 'PATCH'  # Allow partial updates for PATCH
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Loan updated successfully',
                    'data': serializer.data
                })
            
            # Return validation errors
            return Response({
                'success': False,
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle DELETE request
        elif request.method == 'DELETE':
            loan.delete()
            return Response({
                'success': True,
                'message': f'Loan {loan_no} deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        # Handle any unexpected errors
        return Response({
            'success': False,
            'message': 'An error occurred',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)