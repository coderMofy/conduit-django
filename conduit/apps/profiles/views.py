from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer

class ProfileRetrieveAPIView(RetrieveAPIView):
	permission_classes = (AllowAny,)
	renderer_classes = (ProfileJSONRenderer,)
	serializer_class = ProfileSerializer
	

	def get(self, request, username, *args, **kwargs):
		try:
			profile = Profile.objects.select_related('user').get(user__username=username)
		except Profile.DoesNotExist:
			raise ProfileDoesNotExist

		serializer = self.serializer_class(profile)

		return Response(serializer.data, status=status.HTTP_200_OK)


