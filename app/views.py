from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Lga, Ward, PollingUnit, Party, PollingUnitResult
import pandas as pd

# Create your views here.


# copy lgas from csv file to model
def import_lgas(request):

    # read lga csv file to pandas dataframe
    lga_df = pd.read_csv('app/files/lga.csv')

    # iterate over dataframe and save each row to model
    for index, row in lga_df.iterrows():
        lga = Lga(
            uniqueid=row['uniqueid'],
            lga_id=row['lga_id'],
            lga_name=row['lga_name'],
            state_id=row['state_id'],
            lga_description=row['lga_description'],
            entered_by_user=row['entered_by_user'],
            date_entered=row['date_entered'],
            user_ip_address=row['user_ip_address'],
        )
        lga.save()

    # return a success message
    return HttpResponse('Lgas imported successfully')



# copy wards from csv file to model
def import_wards(request):

    # read ward csv file to pandas dataframe
    ward_df = pd.read_csv('app/files/ward.csv')

    # iterate over dataframe and save each row to model
    for index, row in ward_df.iterrows():
        ward = Ward(
            uniqueid=row['uniqueid'],
            ward_id=row['ward_id'],
            ward_name=row['ward_name'],
            lga_id=row['lga_id'],
            ward_description=row['ward_description'],
            entered_by_user=row['entered_by_user'],
            date_entered=row['date_entered'],
            user_ip_address=row['user_ip_address'],
        )
        ward.save()

    # return a success message
    return HttpResponse('Wards imported successfully')



# copy polling units from csv file to model
def import_polling_units(request):

    # read polling unit csv file to pandas dataframe
    polling_unit_df = pd.read_csv('app/files/polling_unit.csv')

    # iterate over dataframe and save each row to model
    for index, row in polling_unit_df.iterrows():
        polling_unit = PollingUnit(
            uniqueid=row['uniqueid'],
            polling_unit_id=row['polling_unit_id'],
            ward_id=row['ward_id'],
            lga_id=row['lga_id'],
            uniquewardid=row['uniquewardid'],
            polling_unit_number=row['polling_unit_number'],
            polling_unit_name=row['polling_unit_name'],
            polling_unit_description=row['polling_unit_description'],
            entered_by_user=row['entered_by_user'],
            date_entered=row['date_entered'],
            user_ip_address=row['user_ip_address'],
        )
        polling_unit.save()

    # return a success message
    return HttpResponse('Polling units imported successfully')



# copy party from csv file to model
def import_parties(request):

    # read party csv file to pandas dataframe
    party_df = pd.read_csv('app/files/party.csv')

    # iterate over dataframe and save each row to model
    for index, row in party_df.iterrows():
        party = Party(
            id=row['id'],
            party_name=row['party_name'],
            
        )
        party.save()

    # return a success message
    return HttpResponse('Parties imported successfully')



# copy polling unit results from csv file to model
def import_polling_unit_results(request):

    # read polling unit results csv file to pandas dataframe
    polling_unit_results_df = pd.read_csv('app/files/polling_unit_results.csv')

    # iterate over dataframe and save each row to model
    for index, row in polling_unit_results_df.iterrows():
        polling_unit_result = PollingUnitResult(
            result_id=row['result_id'],
            polling_unit_uniqueid=row['polling_unit_uniqueid'],
            party_abbreviation=row['party_abbreviation'],
            party_score=row['party_score'],
            entered_by_user=row['entered_by_user'],
            date_entered=row['date_entered'],
            user_ip_address=row['user_ip_address'],
        )
        polling_unit_result.save()

    # return a success message
    return HttpResponse('Polling unit results imported successfully')



#index page
def index(request):
    return render(request, 'index.html')



# view for list of all polling units
def polling_units_list(request):
    
        # get all polling units
        polling_units = PollingUnit.objects.all()
    
        # render list of polling units
        return render(request, 'polling_units_list.html', {'polling_units': polling_units})



# view for a polling unit
def polling_unit_detail(request, uniqueid):
    
        # get polling unit
        polling_unit = PollingUnit.objects.get(uniqueid=uniqueid)

        # get all polling unit results
        polling_unit_results = PollingUnitResult.objects.filter(polling_unit_uniqueid=uniqueid)
        
        #print the results
        print(polling_unit_results)

        # render a polling unit
        return render(request, 'polling_unit_result.html', {'polling_unit': polling_unit, 'polling_unit_results': polling_unit_results})



# view for selecting lga and viewwing results
def select_lga(request):

    #if reququest method is get
    if request.method == 'GET':
    
        # get all lgas
        lgas = Lga.objects.all()
    
        # render list of lgas
        return render(request, 'select_lga.html', {'lgas': lgas})

    #else if request method is post, return sum of lga results per party
    else:

        # get lga id
        lga_id = request.POST['lga']

        # get all polling units
        polling_units = PollingUnit.objects.filter(lga_id=lga_id)
        
        unique_ids = []
        for polling_unit in polling_units:
            unique_ids.append(polling_unit.polling_unit_id)

        # get all polling unit results
        polling_unit_results = PollingUnitResult.objects.filter(polling_unit_uniqueid__in=unique_ids)

        # get all parties
        parties = Party.objects.all()

        # get results for each party
        results_per_party = []
        for party in parties:
            party_results = polling_unit_results.filter(party_abbreviation=party.party_name)
            party_result = {
                'party_id': party.id,
                'party_name': party.party_name,
                'party_score': sum([result.party_score for result in party_results]),
            }
            results_per_party.append(party_result)
            



        # render results
        return render(request, 'lga_result.html', {'results_per_party': results_per_party})


    

# view to add new reults
def add_results(request):
    if request.method == "GET":

        #get all parties
        parties = Party.objects.all()

        #render add results form
        return render(request, 'add_results.html', {'parties': parties})


    # else save submitted data as instance of new polling unit result
    else:
        # get fields from submitted form
        polling_unit_uniqueid = request.POST['polling_unit_uniqueid']
        party_abbreviation = request.POST['party_name']
        party_score = request.POST['party_score']

        # save new polling unit result
        polling_unit_result = PollingUnitResult(
            polling_unit_uniqueid=polling_unit_uniqueid,
            party_abbreviation=party_abbreviation,
            party_score=party_score,
            
        )
        polling_unit_result.save()

        # return a success message
        return HttpResponse('Results added successfully')


