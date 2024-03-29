from sklearn.ensemble import RandomForestClassifier
import urllib3
import logging
import pandas
from warnings import simplefilter
from sklearn.metrics import accuracy_score, multilabel_confusion_matrix
import time
import gc

simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger('intrusion_detection_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





def oneHotEncoding(data):
    logger.info(msg='one hot encoding')
    encodedData = pandas.get_dummies(data)
    return encodedData



def learnToTrainAndTestModel():
    dataframe = pandas.read_csv('../data/test_data.csv')
    headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
               "urgent", "hot", "num_failed_logins" \
        , "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
               "num_access_files", "num_outbound_cmds" \
        , "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
               "srv_rerror_rate", "same_srv_rate" \
        , "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate" \
        , "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "label"]

    dataframe.columns = headers

    encodedData = oneHotEncoding(dataframe)


    encodedLabels = encodedData[
        ['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.',
         'label_ipsweep.', 'label_land.', \
         'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.',
         'label_phf.', 'label_pod.', 'label_portsweep.', \
         'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.',
         'label_warezmaster.']]

    rf = RandomForestClassifier()
    rf.fit(encodedData[['duration', 'logged_in']], encodedLabels)
    predictionsrf = rf.predict(encodedData[['duration', 'logged_in']])
    accuracyScorerf = accuracy_score(encodedLabels, predictionsrf)
    logger.info("accuracy score for model {}:".format(accuracyScorerf))





def trainAndTestModel():
    dataframe = pandas.read_csv('../data/test_data.csv')
    headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
               "urgent", "hot", "num_failed_logins" \
        , "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
               "num_access_files", "num_outbound_cmds" \
        , "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
               "srv_rerror_rate", "same_srv_rate" \
        , "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate" \
        , "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "label"]

    dataframe.columns = headers
    encodedData = oneHotEncoding(dataframe)

    encodedLabels = encodedData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.',\
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.',\
                                  'label_pod.', 'label_portsweep.',\
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]

    logger.info(msg='traing model rf1 on data')
    rf1 = RandomForestClassifier()
    rf1.fit(encodedData[['duration', 'logged_in']], encodedLabels)
    logger.info(msg='training rf1 finished')


    logger.info(msg='training model rf2 on data')
    rf2 = RandomForestClassifier()
    rf2.fit(encodedData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp']], encodedLabels)
    logger.info('training rf2 finised')


    ## basic features
    logger.info(msg='training model rf3 on data')
    rf3 = RandomForestClassifier()
    rf3.fit(encodedData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp',\
                         'service_IRC', 'service_X11', 'service_Z39_50', 'service_auth', 'service_bgp', 'service_courier', \
                         'service_csnet_ns', 'service_ctf', 'service_daytime', 'service_discard', 'service_domain', 'service_domain_u', \
                         'service_echo', 'service_eco_i', 'service_ecr_i', 'service_efs', 'service_exec', 'service_finger', 'service_ftp', \
                         'service_ftp_data', 'service_gopher', 'service_hostnames', 'service_http', 'service_http_443', 'service_imap4', 'service_iso_tsap', \
                         'service_klogin', 'service_kshell', 'service_ldap', 'service_link', 'service_login', 'service_mtp', 'service_name', 'service_netbios_dgm', \
                         'service_netbios_ns', 'service_netbios_ssn', 'service_netstat', 'service_nnsp', 'service_nntp', 'service_ntp_u', 'service_other', 'service_pm_dump',\
                         'service_pop_2', 'service_pop_3', 'service_printer', 'service_private', 'service_red_i', 'service_remote_job', 'service_rje', 'service_shell', 'service_smtp', \
                         'service_sql_net', 'service_ssh', 'service_sunrpc', 'service_supdup', 'service_systat', 'service_telnet', 'service_tftp_u', 'service_tim_i', 'service_time',\
                         'service_urh_i', 'service_urp_i', 'service_uucp', 'service_uucp_path', 'service_vmnet', 'service_whois',\
                         'src_bytes','dst_bytes',\
                         'flag_OTH', 'flag_REJ', 'flag_RSTO', 'flag_RSTOS0', 'flag_RSTR', 'flag_S0', 'flag_S1', 'flag_S2', 'flag_S3', 'flag_SF', 'flag_SH',\
                         'land','wrong_fragment','urgent']], encodedLabels)
    logger.info('training rf3 finised')

    ## content features
    logger.info(msg='training model rf4 on data')
    rf4 = RandomForestClassifier()
    rf4.fit(encodedData[['hot','num_failed_logins','logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', \
                         'num_outbound_cmds', 'is_host_login', 'is_guest_login']], encodedLabels )
    logger.info('training rf4 finished')

    ## traffic features
    logger.info(msg='training model rf5 on data')
    rf5 = RandomForestClassifier()
    rf5.fit(encodedData[['count','serror_rate','rerror_rate','same_srv_rate','diff_srv_rate','srv_count','srv_serror_rate','srv_rerror_rate', 'srv_diff_host_rate']], encodedLabels )
    logger.info('training rf5 finished')





    testDataframe = dataframe
    logger.info('one hot encoding test data')
    encodedTestData = oneHotEncoding(testDataframe)

    ## free up resources used in training
    # uncomment to get confusion matrixes
    del encodedLabels, encodedData, dataframe

    ## predictions
    logger.info('running rf1 on test data')
    predictionsrf1 = rf1.predict(encodedTestData[['duration', 'logged_in']])
    logger.info('running rf2 on test data')
    predictionsrf2 = rf2.predict(encodedTestData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp']])
    logger.info('running rf3 on test data')
    predictionsrf3 = rf3.predict(encodedTestData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp',\
                         'service_IRC', 'service_X11', 'service_Z39_50', 'service_auth', 'service_bgp', 'service_courier', \
                         'service_csnet_ns', 'service_ctf', 'service_daytime', 'service_discard', 'service_domain', 'service_domain_u', \
                         'service_echo', 'service_eco_i', 'service_ecr_i', 'service_efs', 'service_exec', 'service_finger', 'service_ftp', \
                         'service_ftp_data', 'service_gopher', 'service_hostnames', 'service_http', 'service_http_443', 'service_imap4', 'service_iso_tsap', \
                         'service_klogin', 'service_kshell', 'service_ldap', 'service_link', 'service_login', 'service_mtp', 'service_name', 'service_netbios_dgm', \
                         'service_netbios_ns', 'service_netbios_ssn', 'service_netstat', 'service_nnsp', 'service_nntp', 'service_ntp_u', 'service_other', 'service_pm_dump',\
                         'service_pop_2', 'service_pop_3', 'service_printer', 'service_private', 'service_red_i', 'service_remote_job', 'service_rje', 'service_shell', 'service_smtp', \
                         'service_sql_net', 'service_ssh', 'service_sunrpc', 'service_supdup', 'service_systat', 'service_telnet', 'service_tftp_u', 'service_tim_i', 'service_time',\
                         'service_urh_i', 'service_urp_i', 'service_uucp', 'service_uucp_path', 'service_vmnet', 'service_whois',\
                         'src_bytes','dst_bytes',\
                         'flag_OTH', 'flag_REJ', 'flag_RSTO', 'flag_RSTOS0', 'flag_RSTR', 'flag_S0', 'flag_S1', 'flag_S2', 'flag_S3', 'flag_SF', 'flag_SH',\
                         'land','wrong_fragment','urgent']])
    logger.info('running rf4 on test data')
    predictionsrf4 = rf4.predict(encodedTestData[['hot','num_failed_logins','logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', \
                         'num_outbound_cmds', 'is_host_login', 'is_guest_login']])
    logger.info('running rf5 on test data')
    predictionsrf5 = rf5.predict(encodedTestData[['count','serror_rate','rerror_rate','same_srv_rate','diff_srv_rate','srv_count','srv_serror_rate','srv_rerror_rate', 'srv_diff_host_rate']])

    del rf1, rf2, rf3, rf4, rf5
    gc.collect()


    ## encoded test labels
    encodedTestLabels = encodedTestData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.', 'label_portsweep.', \
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]




    logger.info('calculating confusion matrixes')
    ## comparing predictions with the true labels
    #confusionMatrix1 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf1)
    #print(confusionMatrix1)
    #
    # confusionMatrix2 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf2)
    # print(confusionMatrix2)
    #
    # confusionMatrix3 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf3)
    # print(confusionMatrix3)
    #
    # confusionMatrix4 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf4)
    # print(confusionMatrix4)
    #
    # confusionMatrix5 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf5)
    # print(confusionMatrix5)



    logger.info('calcualting accuracy scores')


    accuractyScorerf1 = accuracy_score(encodedTestLabels, predictionsrf1)
    logger.info("accuracy score for model 1: {}".format(accuractyScorerf1))
    accuractyScorerf2 = accuracy_score(encodedTestLabels, predictionsrf2)
    logger.info("accuracy score for model 2: {}".format(accuractyScorerf2))

    accuractyScorerf3 = accuracy_score(encodedTestLabels, predictionsrf3)
    logger.info("accuracy score for model 3: {}".format(accuractyScorerf3))

    accuractyScorerf4 = accuracy_score(encodedTestLabels, predictionsrf4)
    logger.info("accuracy score for model 4: {}".format(accuractyScorerf4))

    accuractyScorerf5 = accuracy_score(encodedTestLabels, predictionsrf5)
    logger.info("accuracy score for model 5: {}".format(accuractyScorerf5))






def main():
    starttime = time.time()
    logger.info('start time: {}'.format(starttime))
    #learnToTrainAndTestModel()
    trainAndTestModel()

    endtime = time.time() - starttime
    logger.info('run time: {}'.format(endtime))



if __name__=="__main__":
    main()