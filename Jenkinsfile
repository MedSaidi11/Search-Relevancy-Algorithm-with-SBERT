pipeline {
    agent any

    environment {
        EC2_INSTANCE_ID = string(credentials("INSTANCE_ID"))
        AWS_REGION = string(credentials("AWS_REGION"))   
        AWS_ACCESS_KEY_ID = string(credentials("AWS_ACCESS_KEY_ID"))
        AWS_SECRET_ACCESS_KEY = string(credentials("SECRET-ACCESS_KEY"))
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'prod', url: 'https://github.com/MedSaidi11/Semantic-Search-Engine-using-Sentence-BERT.git'
            }
        }

        stage('Restart EC2 Instance') {
            steps {
                steps {
                withCredentials([
                    string(credentialsId: 'INSTANCE_ID', variable: 'EC2_INSTANCE_ID'),
                    string(credentialsId: 'AWS_REGION', variable: 'AWS_REGION'),
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'SECRET-ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                script {
                    sh """
                        echo "Rebooting EC2 instance with ID: $EC2_INSTANCE_ID in region: $AWS_REGION"
                        aws ec2 reboot-instances --instance-ids $EC2_INSTANCE_ID --region $AWS_REGION
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker-compose build
                    """
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh """
                        docker-compose up
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Build and deployment successful.'
        }
        failure {
            echo 'There was a failure in the pipeline.'
        }
    }
}
