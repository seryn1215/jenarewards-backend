# Build process

1. Every code changes, should create MR against *develop* branch & merge to deploy automatically by AWS code build
2. if python build dependencies changes expected,
   * we need to rebuild *Dockerfile-base* image with new version manually in local
   * push this new image version in dockerhub capsulehub account,
   * Update the base image version in *Dockerfile*

Info

* AWS Beanstalk
  * [AWS Beanstalk info](https://ap-northeast-2.console.aws.amazon.com/elasticbeanstalk/home?region=ap-northeast-2#/environment/dashboard?environmentId=e-7b3z2ijjyz)
  * App: rewards-backend
  * Env: Rewards-api-dev
* Code build:
  * [AWS Code build-deploy](https://ap-northeast-2.console.aws.amazon.com/codesuite/codebuild/371428749708/projects/rewards-api-dev/history?region=ap-northeast-2)

API Endpoint:

    [https://rewards-api.imcapsule.io/](https://rewards-api.imcapsule.io/)
