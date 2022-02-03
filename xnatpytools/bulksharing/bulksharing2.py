import os
import xnat
import time
import argparse


def get_experiments(args):
    if os.path.isfile(args.experiments):
        with open(args.experiments, 'r') as f:
            experiments = []
            for experiment in f.readlines():
                experiments.append(experiment.strip())
            return experiments
    return [x.strip() for x in args.experiments.split(',')]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Host name of XNAT system, e.g., https://xnat.acc.dh.unimaas.nl')
    parser.add_argument('user', help='Username with admin/owner rights in source project')
    parser.add_argument('password', help='Password')
    parser.add_argument('source_project', help='Project FROM which data is shared')
    parser.add_argument('target_project', help='Project TO which data is shared')
    parser.add_argument('experiments', default=None, help='Text file with experiment ID, or comma-separated list of experiment IDs')
    args = parser.parse_args()

    experiment_ids = get_experiments(args)

    with xnat.connect(server=args.host, user=args.user, password=args.password) as session:

        print(f'Connected to {args.host}')

        source_project = session.projects[args.source_project]
        target_project = session.projects[args.target_project]
        print(f'Found source project {source_project.id} and target project {target_project.id}')

        for experiment_id in experiment_ids:

            subject_id = experiment_id.split('_')[0]
            subject = source_project.subjects[subject_id]

            if subject_id not in target_project.subjects.keys():
                print(f'Sharing subject {subject_id}')
                subject.share(target_project.id, label=subject_id)
            else:
                print(f'Subject {subject_id} already shared with target project')

            experiment = subject.experiments[experiment_id]

            if experiment_id not in target_project.subjects[subject_id].experiments.keys():
                print(f'  Sharing experiment {experiment_id}')
                experiment.share(target_project.id, label=experiment_id)
            else:
                print(f'Experiment {experiment_id} already shared with target project')

            time.sleep(1)


if __name__ == '__main__':
    main()
