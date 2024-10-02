from airflow.providers.telegram.hooks.telegram import TelegramHook # импортируем хук телеграма

def send_telegram_success_message(context): # на вход принимаем словарь со контекстными переменными
    hook = TelegramHook(telegram_conn_id='project_sprint_1',
                        token='7671851950:AAHSwZlN8TyT_t6kOS5_1kg89qw3kGGNMk4',
                        chat_id='-4568038205')
    
    dag = context['dag_id']
    run_id = context['dag_run_id']
    
    message = f'Исполнение DAG {dag} с id={run_id} прошло успешно!' # определение текста сообщения
    
    hook.send_message({
        'chat_id': '-4568038205',
        'text': message
    }) # отправление сообщения

def send_telegram_failure_message(context):
    hook = TelegramHook(telegram_conn_id='project_sprint_1',
                        token='7671851950:AAHSwZlN8TyT_t6kOS5_1kg89qw3kGGNMk4',
                        chat_id='-4568038205')

    dag = context['dag']
    run_id = context['run_id']
    task_instance_key_str = context['task_instance_key_str']
    
    message = f'СТАТУС task_instance_key_str={task_instance_key_str}: DAG {dag} с id={run_id} ПОТРАЧЕНО!' # определение текста сообщения
    hook.send_message({
        'chat_id': '-4568038205',
        'text': message
    }) # отправление сообщения