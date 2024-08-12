import graphene
from graphene_django import DjangoObjectType, DjangoListField
from forms.models import Form, Question


class FormGQL(DjangoObjectType):
    class Meta:
        model = Form
        exclude = ["password"]


class QuestionGQL(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"


class Query(graphene.ObjectType):
    form_info = graphene.Field(FormGQL, id=graphene.Int())

    form_question = DjangoListField(QuestionGQL, id=graphene.Int())

    def resolve_form_question(root, info, id):
        forms = Form.objects.filter(pk=id).first()
        questions = Question.objects.filter(form=forms)
        if forms:
            forms.visitor_count += 1
            forms.save()
        return questions

    def resolve_form_info(root, info, id):
        form = Form.objects.filter(pk=id).first()
        return form


schema = graphene.Schema(query=Query)
