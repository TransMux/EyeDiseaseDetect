import CloudUploadIcon from '@/assets/upload.svg';
import Layout from '@/layouts';
import ChartBar from '@/assets/chart-bar.svg';

export default [
  {
    path: '/upload',
    redirect: '/upload/base',
    component: Layout,
    meta: { title: 'Upload', icon: CloudUploadIcon, single: true },
    children: [
      {
        path: 'base',
        name: 'uploadbase',
        component: () => import('@/pages/Upload/index.vue'),
      },
    ],
  },
  {
    path: '/detect',
    component: Layout,
    name: 'detection',
    redirect: '/detect/base',
    meta: { title: 'Detection', icon: ChartBar, single: true },
    children: [
      {
        path: 'base',
        name: 'detectBase',
        component: () => import('@/pages/Detect/tree/index.vue'),
      },
    ],
  },
];
