import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { S3BaseStack } from './stack/s3-stack';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class MoneybookStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new S3BaseStack(this, 's3Stack', props);
  }
}