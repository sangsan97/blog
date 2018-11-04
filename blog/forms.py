from django import forms
from .models import Post, Publication, Comment, MyUser, Member
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import datetime

class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'StudentID']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = ('author', 'where_to_status', 'title', 'text', 'document', 'photo')
        fields = ('where_to_status', 'title', 'text', 'document', 'photo')

    # def __init__(self):
    #     super().__init__()
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Save'))


# Form for publication 
current_year = datetime.now().year
until_current_year = tuple([i for i in reversed(range(current_year-30, current_year+1))])

class PublicationForm(forms.ModelForm):
    
    class Meta:
        model = Publication
        fields = ('title', 'author','explanation_for_the_publication', 'year_of_publication', 'link_url')
        widgets = {
            'year_of_publication' : forms.SelectDateWidget(years=until_current_year),

        }

class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = {'name', 'where_to_status', 'text', 'photo', }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }