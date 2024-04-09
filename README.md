# djangoRest

# Notes
1- In validators we have 3 types of validaters:
- field level
- object level
- validator passed as an argument

2- Permission access:
- Active: Meaning that the user us authenticated and can log in to application but not admin panel.
- Staff: Meaning the the user can log in to the admin panel also. 
- Superuser: Meaning that the user can do any action in the admin panel this of course can be limited through permissions.

3- Permission Combinations:
- NONE: Meaning that I have stored the user credentials but he can't neither access the application or the admin panel.
- Active only: user can login to app but not admin panel
- Staff only: User can login to admin panel.
- superuser: User can do any admin panel action
- Staff with permissions: User do only specific permision from the super user actions.

4- overriding create vs overriding perform-create:
- When you override the create method directly, you don't necessarily need to define a queryset attribute or override the get_queryset() method. This is because the create method is responsible for creating a new object, and it doesn't directly involve querying existing objects from the database.
- However, when you override the perform_create method, as you did in your original code, you still need to ensure that the queryset attribute or get_queryset() method is defined, as this method might interact with the database indirectly, such as checking for the existence of related objects or fetching related objects for validation purposes.
- In your original code, you're indirectly interacting with the database within the perform_create method by fetching the WatchList object using WatchList.objects.get(pk=pk). Therefore, Django REST Framework still expects a queryset attribute or get_queryset() method to be defined, as it needs to ensure consistency and provide flexibility for handling such cases.
- To summarize, when you override methods like perform_create or update, which might interact with the database indirectly, it's necessary to ensure that either a queryset attribute or a get_queryset() method is defined to maintain the expected behavior and to avoid errors like the one you encountered.

5- Authentication Types:
- Basic authentication
- token authentication

# Start From
5. 19. Viewsets ==> 4:52
