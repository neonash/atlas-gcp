# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AtlasAggtaggeddata(models.Model):
    dataset_filename = models.CharField(max_length=100)
    rid = models.CharField(max_length=155)
    dim1 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    aid = models.ForeignKey('AtlasSocial', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_aggtaggeddata'


class AtlasAggtaggeddatarev(models.Model):
    pcategory = models.CharField(db_column='pCategory', max_length=100)  # Field name made lowercase.
    dim1 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    rid = models.ForeignKey('AtlasReview', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_aggtaggeddatarev'


class AtlasAggtaggeddataupl(models.Model):
    dataset_filename = models.CharField(max_length=100)
    dim1 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    rid = models.ForeignKey('AtlasUploads', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_aggtaggeddataupl'


class AtlasAnalysis(models.Model):
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    sentiscore = models.DecimalField(db_column='sentiScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    trigger = models.CharField(max_length=200, blank=True, null=True)
    driver = models.CharField(max_length=200, blank=True, null=True)
    rid = models.ForeignKey('AtlasReview', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_analysis'


class AtlasContentcategoryrev(models.Model):
    category_pri = models.CharField(max_length=200, blank=True, null=True)
    category_sec = models.CharField(max_length=200, blank=True, null=True)
    category_ter = models.CharField(max_length=200, blank=True, null=True)
    confidence = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    rid = models.ForeignKey('AtlasReview', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_contentcategoryrev'


class AtlasContentcategorysoc(models.Model):
    category_pri = models.CharField(max_length=200, blank=True, null=True)
    category_sec = models.CharField(max_length=200, blank=True, null=True)
    category_ter = models.CharField(max_length=200, blank=True, null=True)
    confidence = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    rid = models.ForeignKey('AtlasSocial', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_contentcategorysoc'


class AtlasContentcategoryupl(models.Model):
    category_pri = models.CharField(max_length=200, blank=True, null=True)
    category_sec = models.CharField(max_length=200, blank=True, null=True)
    category_ter = models.CharField(max_length=200, blank=True, null=True)
    confidence = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    rid = models.ForeignKey('AtlasUploads', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_contentcategoryupl'


class AtlasDimenmap(models.Model):
    dict_filename = models.CharField(primary_key=True, max_length=255)
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_dimenmap'


class AtlasDimenmapupl(models.Model):
    dict_filename = models.CharField(primary_key=True, max_length=255)
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_dimenmapupl'


class AtlasProduct(models.Model):
    pid = models.CharField(primary_key=True, max_length=100)
    pcategory = models.CharField(db_column='pCategory', max_length=30)  # Field name made lowercase.
    pbrand = models.CharField(db_column='pBrand', max_length=30)  # Field name made lowercase.
    pdescr = models.TextField(db_column='pDescr')  # Field name made lowercase.
    prating = models.DecimalField(db_column='pRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    pimgsrc = models.TextField(db_column='pImgSrc')  # Field name made lowercase.
    pmodel = models.CharField(db_column='pModel', max_length=30)  # Field name made lowercase.
    ptitle = models.TextField(db_column='pTitle')  # Field name made lowercase.
    purl = models.TextField(db_column='pURL')  # Field name made lowercase.
    pprice = models.CharField(db_column='pPrice', max_length=10)  # Field name made lowercase.
    sitecode = models.CharField(db_column='siteCode', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'atlas_product'


class AtlasRequests(models.Model):
    reqkw = models.TextField(db_column='reqKw')  # Field name made lowercase.
    reqtime = models.DateTimeField(db_column='reqTime', blank=True, null=True)  # Field name made lowercase.
    reqstatus = models.TextField(db_column='reqStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'atlas_requests'


class AtlasReview(models.Model):
    rid = models.CharField(primary_key=True, max_length=100)
    rdate = models.IntegerField(db_column='rDate')  # Field name made lowercase.
    rdate2 = models.DateField(db_column='rDate2', blank=True, null=True)  # Field name made lowercase.
    rrating = models.DecimalField(db_column='rRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    rtext = models.TextField(db_column='rText')  # Field name made lowercase.
    rtitle = models.TextField(db_column='rTitle')  # Field name made lowercase.
    rurl = models.TextField(db_column='rURL')  # Field name made lowercase.
    ruser = models.CharField(db_column='rUser', max_length=30)  # Field name made lowercase.
    pid = models.ForeignKey(AtlasProduct, models.DO_NOTHING)
    dt = models.CharField(max_length=2, blank=True, null=True)
    mth = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_review'


class AtlasSocial(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    dataset_filename = models.CharField(max_length=100)
    rid = models.CharField(max_length=100)
    rtitle = models.TextField(db_column='rTitle', blank=True, null=True)  # Field name made lowercase.
    ruser = models.TextField(db_column='rUser', blank=True, null=True)  # Field name made lowercase.
    rtext = models.TextField(db_column='rText', blank=True, null=True)  # Field name made lowercase.
    rurl = models.TextField(db_column='rURL', blank=True, null=True)  # Field name made lowercase.
    rrating = models.DecimalField(db_column='rRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    media_provider = models.TextField(db_column='MEDIA_PROVIDER', blank=True, null=True)  # Field name made lowercase.
    rdate = models.IntegerField(db_column='rDate', blank=True, null=True)  # Field name made lowercase.
    rdate2 = models.DateField(db_column='rDate2', blank=True, null=True)  # Field name made lowercase.
    view_count = models.IntegerField(db_column='VIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
    comment_count = models.IntegerField(db_column='COMMENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    unique_commenters = models.IntegerField(db_column='UNIQUE_COMMENTERS', blank=True, null=True)  # Field name made lowercase.
    engagement = models.IntegerField(db_column='ENGAGEMENT', blank=True, null=True)  # Field name made lowercase.
    links_and_votes = models.IntegerField(db_column='LINKS_AND_VOTES', blank=True, null=True)  # Field name made lowercase.
    inbound_links = models.IntegerField(db_column='INBOUND_LINKS', blank=True, null=True)  # Field name made lowercase.
    forum_thread_size = models.IntegerField(db_column='FORUM_THREAD_SIZE', blank=True, null=True)  # Field name made lowercase.
    following = models.IntegerField(db_column='FOLLOWING', blank=True, null=True)  # Field name made lowercase.
    followers = models.IntegerField(db_column='FOLLOWERS', blank=True, null=True)  # Field name made lowercase.
    updates = models.IntegerField(db_column='UPDATES', blank=True, null=True)  # Field name made lowercase.
    blog_post_sentiment = models.CharField(db_column='BLOG_POST_SENTIMENT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    dt = models.CharField(max_length=2, blank=True, null=True)
    mth = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_social'


class AtlasSocialanalyses(models.Model):
    rid = models.CharField(max_length=155)
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    sentiscore = models.DecimalField(db_column='sentiScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    trigger = models.CharField(max_length=200, blank=True, null=True)
    driver = models.CharField(max_length=200, blank=True, null=True)
    aid = models.ForeignKey(AtlasSocial, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_socialanalyses'


class AtlasTagdicts(models.Model):
    ngram = models.CharField(max_length=155)
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)
    dict_filename = models.ForeignKey(AtlasDimenmap, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_tagdicts'


class AtlasTagdictsupl(models.Model):
    ngram = models.CharField(max_length=155)
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)
    dict_filename = models.ForeignKey(AtlasDimenmap, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_tagdictsupl'


class AtlasTaggeddata(models.Model):
    dataset_filename = models.CharField(max_length=100)
    rid = models.CharField(max_length=155)
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)
    aid = models.ForeignKey(AtlasSocial, models.DO_NOTHING)
    ngram = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_taggeddata'


class AtlasTaggeddatarev(models.Model):
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)
    rid = models.ForeignKey(AtlasReview, models.DO_NOTHING)
    pcategory = models.CharField(db_column='pCategory', max_length=100)  # Field name made lowercase.
    ngram = models.CharField(max_length=155, blank=True, null=True)
    dict_filename = models.ForeignKey(AtlasDimenmap, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_taggeddatarev'


class AtlasTaggeddataupl(models.Model):
    dim1 = models.TextField(blank=True, null=True)
    d1_l1 = models.TextField(blank=True, null=True)
    d1_l2 = models.TextField(blank=True, null=True)
    d1_l3 = models.TextField(blank=True, null=True)
    d1_l4 = models.TextField(blank=True, null=True)
    d1_l5 = models.TextField(blank=True, null=True)
    dim2 = models.TextField(blank=True, null=True)
    d2_l1 = models.TextField(blank=True, null=True)
    d2_l2 = models.TextField(blank=True, null=True)
    d2_l3 = models.TextField(blank=True, null=True)
    d2_l4 = models.TextField(blank=True, null=True)
    d2_l5 = models.TextField(blank=True, null=True)
    dim3 = models.TextField(blank=True, null=True)
    d3_l1 = models.TextField(blank=True, null=True)
    d3_l2 = models.TextField(blank=True, null=True)
    d3_l3 = models.TextField(blank=True, null=True)
    d3_l4 = models.TextField(blank=True, null=True)
    d3_l5 = models.TextField(blank=True, null=True)
    dim4 = models.TextField(blank=True, null=True)
    d4_l1 = models.TextField(blank=True, null=True)
    d4_l2 = models.TextField(blank=True, null=True)
    d4_l3 = models.TextField(blank=True, null=True)
    d4_l4 = models.TextField(blank=True, null=True)
    d4_l5 = models.TextField(blank=True, null=True)
    dim5 = models.TextField(blank=True, null=True)
    d5_l1 = models.TextField(blank=True, null=True)
    d5_l2 = models.TextField(blank=True, null=True)
    d5_l3 = models.TextField(blank=True, null=True)
    d5_l4 = models.TextField(blank=True, null=True)
    d5_l5 = models.TextField(blank=True, null=True)
    dim6 = models.TextField(blank=True, null=True)
    d6_l1 = models.TextField(blank=True, null=True)
    d6_l2 = models.TextField(blank=True, null=True)
    d6_l3 = models.TextField(blank=True, null=True)
    d6_l4 = models.TextField(blank=True, null=True)
    d6_l5 = models.TextField(blank=True, null=True)
    dim7 = models.TextField(blank=True, null=True)
    d7_l1 = models.TextField(blank=True, null=True)
    d7_l2 = models.TextField(blank=True, null=True)
    d7_l3 = models.TextField(blank=True, null=True)
    d7_l4 = models.TextField(blank=True, null=True)
    d7_l5 = models.TextField(blank=True, null=True)
    dim8 = models.TextField(blank=True, null=True)
    d8_l1 = models.TextField(blank=True, null=True)
    d8_l2 = models.TextField(blank=True, null=True)
    d8_l3 = models.TextField(blank=True, null=True)
    d8_l4 = models.TextField(blank=True, null=True)
    d8_l5 = models.TextField(blank=True, null=True)
    dim9 = models.TextField(blank=True, null=True)
    d9_l1 = models.TextField(blank=True, null=True)
    d9_l2 = models.TextField(blank=True, null=True)
    d9_l3 = models.TextField(blank=True, null=True)
    d9_l4 = models.TextField(blank=True, null=True)
    d9_l5 = models.TextField(blank=True, null=True)
    dim10 = models.TextField(blank=True, null=True)
    d10_l1 = models.TextField(blank=True, null=True)
    d10_l2 = models.TextField(blank=True, null=True)
    d10_l3 = models.TextField(blank=True, null=True)
    d10_l4 = models.TextField(blank=True, null=True)
    d10_l5 = models.TextField(blank=True, null=True)
    dim11 = models.TextField(blank=True, null=True)
    d11_l1 = models.TextField(blank=True, null=True)
    d11_l2 = models.TextField(blank=True, null=True)
    d11_l3 = models.TextField(blank=True, null=True)
    d11_l4 = models.TextField(blank=True, null=True)
    d11_l5 = models.TextField(blank=True, null=True)
    dim12 = models.TextField(blank=True, null=True)
    d12_l1 = models.TextField(blank=True, null=True)
    d12_l2 = models.TextField(blank=True, null=True)
    d12_l3 = models.TextField(blank=True, null=True)
    d12_l4 = models.TextField(blank=True, null=True)
    d12_l5 = models.TextField(blank=True, null=True)
    dim13 = models.TextField(blank=True, null=True)
    d13_l1 = models.TextField(blank=True, null=True)
    d13_l2 = models.TextField(blank=True, null=True)
    d13_l3 = models.TextField(blank=True, null=True)
    d13_l4 = models.TextField(blank=True, null=True)
    d13_l5 = models.TextField(blank=True, null=True)
    dim14 = models.TextField(blank=True, null=True)
    d14_l1 = models.TextField(blank=True, null=True)
    d14_l2 = models.TextField(blank=True, null=True)
    d14_l3 = models.TextField(blank=True, null=True)
    d14_l4 = models.TextField(blank=True, null=True)
    d14_l5 = models.TextField(blank=True, null=True)
    dim15 = models.TextField(blank=True, null=True)
    d15_l1 = models.TextField(blank=True, null=True)
    d15_l2 = models.TextField(blank=True, null=True)
    d15_l3 = models.TextField(blank=True, null=True)
    d15_l4 = models.TextField(blank=True, null=True)
    d15_l5 = models.TextField(blank=True, null=True)
    rid = models.ForeignKey('AtlasUploads', models.DO_NOTHING)
    dataset_filename = models.CharField(max_length=255)
    ngram = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_taggeddataupl'


class AtlasUploadanalyses(models.Model):
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    sentiscore = models.DecimalField(db_column='sentiScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    trigger = models.CharField(max_length=200, blank=True, null=True)
    driver = models.CharField(max_length=200, blank=True, null=True)
    rid = models.ForeignKey('AtlasUploads', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'atlas_uploadanalyses'


class AtlasUploads(models.Model):
    rid = models.CharField(primary_key=True, max_length=100)
    rdate = models.IntegerField(db_column='rDate', blank=True, null=True)  # Field name made lowercase.
    rdate2 = models.DateField(db_column='rDate2', blank=True, null=True)  # Field name made lowercase.
    rrating = models.DecimalField(db_column='rRating', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    rtext = models.TextField(db_column='rText')  # Field name made lowercase.
    rtitle = models.TextField(db_column='rTitle', blank=True, null=True)  # Field name made lowercase.
    rurl = models.TextField(db_column='rURL', blank=True, null=True)  # Field name made lowercase.
    ruser = models.CharField(db_column='rUser', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pcategory = models.CharField(db_column='pCategory', max_length=100)  # Field name made lowercase.
    dt = models.CharField(max_length=2, blank=True, null=True)
    mth = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atlas_uploads'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
