from django.db import models
import django
from django.db.models import Count



class AlreadyExists(Exception):
    pass

class DoesNotExists(Exception):
    pass

def parse_filter_args(params):
    dct = {}
    for k,v in params.iteritems():
        if k.endswith("~"):
            dct[k.replace("~", "__icontains")] = v
        else:
            dct[k] = v
    return dct


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def to_dict(self):
        dt = self.__dict__.copy()
        dt.pop("_state")
        return dt

    @classmethod
    def _create(cls, **params):
        
        if cls.id_attr in params:
            _id = {cls.id_attr : params.get(cls.id_attr)}
            if cls.objects.filter(**_id).exists():
                raise AlreadyExists("The {} with {} id is already exists in records".format(cls.__name__, cls.id_attr))
        try:
            obj = cls(
                **params
            )
            obj.save()
        except:
            raise
        return obj.to_dict()

    @classmethod
    def _update(cls, key, **params):
        _id = {cls.id_attr : key}
        if not cls.objects.get(**_id):
            raise DoesNotExists("The {} with {} is doesn't exists in records".format(cls.__name__, key))
        params[cls.id_attr] = key
        obj = cls(
            **params
        )
        obj.save()
        return obj.to_dict()

    @classmethod
    def _unique(cls, attr_name, **filter_params):
        res = cls.objects.values(attr_name)\
            .filter(**filter_params)
        l = tuple(i for i in res)
        return {"data" : l}


    @classmethod
    def _filter(cls, **params):
        filt = cls.objects.filter(**parse_filter_args(params))
        return {"data" : [o.to_dict() for o in filt] }

    @classmethod
    def _get(cls, key):
        _id = {cls.id_attr : key}
        filt = cls.objects.get(**_id)
        return filt.to_dict()


class User(BaseModel):
    name = models.CharField(max_length = 150)
    user_id = models.CharField(primary_key = True,max_length = 150)
    password = models.CharField(max_length=10)
    
    class Meta:
        db_table = "user"

    id_attr =  "user_id"

    @classmethod
    def _create(cls,**params):
        return super(User, cls)._create(**params)

    @classmethod
    def _filter(cls, **params):
        return super(User, cls)._filter(**params)

    @classmethod
    def _update(cls,key, **params):
        return super(User, cls)._update(key, **params)

    @classmethod
    def _unique(cls,attr, **params):
        return super(User, cls)._unique(attr, **params)

    @classmethod
    def _get(cls, val):
        return super(User, cls)._get(val)


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = "post"

    id_attr = "post_id"

    @classmethod
    def _create(cls,**params):
        return super(Post, cls)._create(**params)

    @classmethod
    def _filter(cls, **params):
        return super(Post, cls)._filter(**params)

    @classmethod
    def _update(cls,key, **params):
        return super(Post, cls)._update(key, **params)

    @classmethod
    def _unique(cls,attr, **params):
        return super(Post, cls)._unique(attr, **params)

    @classmethod
    def _get(cls, val):
        return super(Post, cls)._get(val)



class Reaction(BaseModel):
    REACTION_TYPES = (
        ('L', 'Like'),
        ('D', 'Dislike')
    )
    reaction_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reacted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=1, choices=REACTION_TYPES)
    
    class Meta:
        db_table = "reaction"
        unique_together = (('post', 'reacted_user'),)

    id_attr = "reaction_id"

    @classmethod
    def _create(cls,**params):
        return super(Reaction, cls)._create(**params)

    @classmethod
    def _filter(cls, **params):
        return super(Reaction, cls)._filter(**params)

    @classmethod
    def _update(cls,key, **params):
        return super(Reaction, cls)._update(key, **params)

    @classmethod
    def _unique(cls, attr, **params):
        return super(Reaction, cls)._unique(attr, **params)

    @classmethod
    def _get(cls, val):
        return super(Reaction, cls)._get(val)


"""
class Company(models.Model):
    company_name = models.CharField(primary_key = True,max_length = 150)
    building_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    class Meta:
        db_table = "company"

    def to_dict(self):
        dt = self.__dict__.copy()
        dt.pop("_state")
        return dt

    @classmethod
    def _update(cls, company_name, **params):
        if not cls.objects.filter(company_name = company_name).exists():
            raise CompanyDoesNotExists("The company name with {} is doesn't exists in records".format(company_name))
        new_company = cls(
            company_name = company_name,
            **params
        )
        new_company.save()
        return new_company.to_dict()

    @classmethod
    def _delete(cls, company_name):
        filt =cls.objects.filter(company_name = company_name)
        if not filt.exists():
            raise CompanyDoesNotExists("The company name with {} is doesn't exists in records".format(company_name))
        filt.delete()
        return True

    @classmethod
    def _unique(cls, attr_name, count = 1, condition_type = "gt"):
        res = cls.objects.values(attr_name)\
            .annotate( **{ "{}_count".format(attr_name) : Count(attr_name) })\
            .filter(**{"{}_count{}".format(attr_name, "" if condition_type == "eq" else "__"+condition_type) : int(count) }) 
        l = tuple(i for i in res)
        return {"data" : l}

"""
