"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from atlas import views
from atlas import summary, analysis, clustering


urlpatterns = [
    url(r'^product/$', views.searchQuery),
    url(r'^product/add$', views.addProduct),
    url(r'^product/(\w+\s*\w*)/refresh$', views.refreshProduct),
    url(r'^request/$', views.getRequests),  # to use jsGrid to plainly load request.csv
    url(r'^request1/$', views.getRequests1),  # to use angularjs to load request.csv with download links
    url(r'^download_tagdata/$', views.download_tag_file),
    url(r'^download_ngrams/$', views.download_ngram_file),
    url(r'^download_rawdata/$', views.download_raw_data),
    url(r'^download_contcat/$', views.download_contcat_data),
    url(r'^product_list/$', views.getAutoCompleteList),
    url(r'^upload/$', views.uploadFile),
    url(r'^start/$', views.start_analysis),
    url(r'^readdims/$', views.read_dims),
    url(r'^testscrape/$', views.testscrape),

    url(r'^summary_countRevCards/$', summary.getCountRevCardsData),
    url(r'^summary_countRevCardsOverall/$', summary.getCountRevCardsOverallData),
    url(r'^summary_toppos_posts/$', summary.getTopposPostsData),
    url(r'^summary_topposposts_overall/$', summary.getTopposOverallData),
    url(r'^summary_topneg_posts/$', summary.getTopnegPostsData),
    url(r'^summary_topnegposts_overall/$', summary.getTopnegOverallData),
    url(r'^summary_topposneg/$', summary.getTopposnegData),
    url(r'^summary_topposnegOverall/$', summary.getTopposnegOverallData),
    url(r'^summary_brand1/$', summary.getBrandFilter),
    url(r'^summary_source1/$', summary.getSourceFilter),
    url(r'^summary_source1_revmap/$', summary.getSourceRevmap),  # source reverse mapping to get siteCode from siteName
    url(r'^summary_sku1/$', summary.getSkuFilter),
    url(r'^summary_chart1/$', summary.getChart1Data),
    url(r'^summary_common_reviewcount_chart/$', summary.getCommonReviewCountChartData),
    #url(r'^summary_chart2/$', summary.getChart2Data),
    url(r'^summary_chart3/$', summary.getChart3Data),
    url(r'^summary_piechart/$', summary.getPieChartData),
    url(r'^summary_categchart_rev/$', summary.getCategChartRevData),
    url(r'^summary_categchart/$', summary.getCategChartData),
    url(r'^summary_wordcloud_rev/$', summary.getWordCloudRevData),
    url(r'^summary_wordcloud/$', summary.getWordCloudData),

    url(r'^analysis_brand1/$', analysis.getBrandFilter),
    url(r'^analysis_reload_brand_with_src/$', analysis.reloadBrandFilterWithSrc),
    url(r'^analysis_reload_brand_with_sku/$', analysis.reloadBrandFilterWithSku),
    url(r'^analysis_source1/$', analysis.getSourceFilter),
    url(r'^analysis_reload_src_with_brd/$', analysis.reloadSourceFilterWithBrd),
    url(r'^analysis_reload_src_with_sku/$', analysis.reloadSourceFilterWithSku),
    url(r'^analysis_sku1/$', analysis.getSkuFilter),
    url(r'^analysis_reload_sku_with_brd/$', analysis.reloadSkuFilterWithBrd),
    url(r'^analysis_reload_sku_with_src/$', analysis.reloadSkuFilterWithSrc),
    url(r'^analysis_brandsummary_chart/$', analysis.getBrandSummaryChartData),
    url(r'^analysis_chart1/$', analysis.getChart1Data),
    url(r'^analysis_chart2/$', analysis.getChart2Data),
    url(r'^analysis_chart3/$', analysis.getChart3Data),
    url(r'^analysis_common_trig_chart/$', analysis.getCommonTrigChartData),
    url(r'^analysis_chart4/$', analysis.getChart4Data),
    url(r'^analysis_common_driv_chart/$', analysis.getCommonDrivChartData),
    url(r'^analysis_common_senti_chart/$', analysis.getCommonSentiChartData),

    url(r'^clustering_data/$', clustering.getReviewClusteringData),
    url(r'^clustering_data_social/$', clustering.getSocialClusteringData),
    url(r'^clustering_data_upload/$', clustering.getUploadClusteringData),

    url(r'^pivotparser/$', summary.getPivotdata),

    url(r'^assoc_dims/$', summary.getAssocDims),
    url(r'^assoc_levels/$', summary.getAssocLevels),
    url(r'^association/$', summary.getAssociationMapdata),
]

