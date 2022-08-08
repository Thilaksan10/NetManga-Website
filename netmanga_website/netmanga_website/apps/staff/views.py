from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader

from ..accounts.models import WithdrawOrder, ReportOneShot, ReportChapter

class WithdrawOrderInfo:
    def __init__(self, date, order):
        self.date = date
        self.order = order

def process_withdraws(request):
    template = loader.get_template('staff/process_withdraws.html')
    if request.method == 'GET':
        if request.user.is_staff:
            withdraw_orders = WithdrawOrder.objects.all().order_by('date_time')
            pending_order_infos = []
            failed_order_infos = []
            succeeded_order_infos = []
            if withdraw_orders:
                
                for i in range(0,len(withdraw_orders)):
                    #print(withdraw_orders[i].date_time.strftime('%d.%m.%y'), flush = True)
                    #print(withdraw_orders[i-1].date_time.strftime('%d.%m.%y'), flush = True)
                    if withdraw_orders[i].status == 'Pending':
                        if len(pending_order_infos) == 0:
                            pending_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                pending_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                pending_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
                    elif withdraw_orders[i].status == 'Failed':
                        if len(failed_order_infos) == 0:
                            failed_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                failed_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                failed_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
                    else:
                        if len(succeeded_order_infos) == 0:
                            succeeded_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                succeeded_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                succeeded_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
            return HttpResponse(template.render({'pending_order_infos':pending_order_infos, 'failed_order_infos': failed_order_infos, 'succeeded_order_infos': succeeded_order_infos}, request))
        else:
            return HttpResponseRedirect('')

def process_withdrawal(request, pk):
    template = loader.get_template('staff/process_withdraws.html')
    withdraw_order = WithdrawOrder.objects.filter(pk=pk).first()
    if request.method == 'GET':
        if request.user.is_staff:
            withdraw_orders = WithdrawOrder.objects.all().order_by('date_time')
            if withdraw_orders:
                pending_order_infos = []
                failed_order_infos = []
                succeeded_order_infos = []
                for i in range(0,len(withdraw_orders)):
                    if withdraw_orders[i].status == 'Pending':
                        if len(pending_order_infos) == 0:
                            pending_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                pending_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                pending_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
                    elif withdraw_orders[i].status == 'Failed':
                        if len(failed_order_infos) == 0:
                            failed_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                failed_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                failed_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
                    else:
                        if len(succeeded_order_infos) == 0:
                            succeeded_order_infos = [WithdrawOrderInfo(True, withdraw_orders[i])]
                        else:
                            if withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y'):
                                succeeded_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                            else:
                                succeeded_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
            return HttpResponse(template.render({'pending_order_infos':pending_order_infos, 'failed_order_infos': failed_order_infos, 'succeeded_order_infos': succeeded_order_infos, 'withdraw_order': withdraw_order}, request))
        else:
            return HttpResponseRedirect('')
    elif request.method == 'POST':
        pass
    pass

def process_reports(request):
    template = loader.get_template('staff/process_reports.html')
    if request.method == 'GET':
        if request.user.is_staff:
            return HttpResponse(template.render({}, request))
        else:
            return HttpResponseRedirect('')
    elif request.method == 'POST':
        pass
    pass