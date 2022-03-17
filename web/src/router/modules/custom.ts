import Layout from '@/layouts';
import ChartBar from '@/assets/chart-bar.svg';

export default [
    {
        path: '/detect',
        component: Layout,
        name: 'detection',
        redirect: '/detect/base',
        meta: { title: '检测', icon: ChartBar, single: true },
        children: [
            {
                path: 'base',
                name: 'detectBase',
                component: () => import('@/pages/Detect/tree/index.vue'),
            },
        ],
    },
];
