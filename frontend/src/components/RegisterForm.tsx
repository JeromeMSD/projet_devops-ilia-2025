import { useState, type ComponentProps } from 'react';
import { Link, useNavigate } from 'react-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Field,
    FieldDescription,
    FieldError,
    FieldGroup,
    FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { registerSchema, roles, type RegisterFormValues } from '@/auth/schema/register-schema.ts';
import { useRegister } from '@/auth/useRegister';
import { useLogin } from '@/auth/useLogin';

export function RegisterForm({ className, ...props }: ComponentProps<'div'>) {
    const navigate = useNavigate();
    const registerMutation = useRegister();
    const login = useLogin();
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [autoLoginError, setAutoLoginError] = useState<string | null>(null);

    const form = useForm<RegisterFormValues>({
        resolver: zodResolver(registerSchema),
        defaultValues: {
            firstname: '',
            lastname: '',
            email: '',
            password: '',
            role: 'USER',
        },
    });

    async function onSubmit(values: RegisterFormValues) {
        registerMutation.reset();
        login.reset();
        setSuccessMessage(null);
        setAutoLoginError(null);

        let data;
        try {
            data = await registerMutation.mutateAsync(values);
        } catch {
            return;
        }

        setSuccessMessage(data.message ?? 'Compte créé avec succès !');
        form.reset({
            firstname: '',
            lastname: '',
            email: '',
            password: '',
            role: 'USER',
        });

        try {
            await login.mutateAsync({
                email: values.email,
                password: values.password,
            });
            navigate('/dashboard');
        } catch (error) {
            const message = error instanceof Error
                ? error.message
                : 'Connexion automatique impossible';
            setAutoLoginError(message);
        }
    }

    const registerError = registerMutation.error instanceof Error ? registerMutation.error.message : null;
    const loginError = autoLoginError ?? (login.error instanceof Error ? login.error.message : null);
    const apiErrors = [registerError, loginError].filter((message): message is string => Boolean(message));
    const isBusy = registerMutation.isPending || login.isPending;

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Créer un compte</CardTitle>
                    <CardDescription>
                        Renseignez vos informations pour accéder à la plateforme.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-6"
                        noValidate
                    >
                        <FieldGroup>
                            <div className="grid gap-4 md:grid-cols-2">
                                <Controller
                                    name="firstname"
                                    control={form.control}
                                    render={({ field, fieldState }) => (
                                        <Field data-invalid={fieldState.invalid}>
                                            <FieldLabel htmlFor="firstname">Prénom</FieldLabel>
                                            <Input
                                                {...field}
                                                id="firstname"
                                                type="text"
                                                placeholder="Simon"
                                                aria-invalid={fieldState.invalid}
                                                disabled={isBusy}
                                            />
                                            {fieldState.invalid && (
                                                <FieldError errors={[fieldState.error]} />
                                            )}
                                        </Field>
                                    )}
                                />

                                <Controller
                                    name="lastname"
                                    control={form.control}
                                    render={({ field, fieldState }) => (
                                        <Field data-invalid={fieldState.invalid}>
                                            <FieldLabel htmlFor="lastname">Nom</FieldLabel>
                                            <Input
                                                {...field}
                                                id="lastname"
                                                type="text"
                                                placeholder="Pierre"
                                                aria-invalid={fieldState.invalid}
                                                disabled={isBusy}
                                            />
                                            {fieldState.invalid && (
                                                <FieldError errors={[fieldState.error]} />
                                            )}
                                        </Field>
                                    )}
                                />
                            </div>

                            <Controller
                                name="email"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="register-email">Adresse email</FieldLabel>
                                        <Input
                                            {...field}
                                            id="register-email"
                                            type="email"
                                            placeholder="simon.pierre@example.com"
                                            aria-invalid={fieldState.invalid}
                                            disabled={isBusy}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            <Controller
                                name="password"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="register-password">Mot de passe</FieldLabel>
                                        <Input
                                            {...field}
                                            id="register-password"
                                            type="password"
                                            placeholder="Password123"
                                            aria-invalid={fieldState.invalid}
                                            disabled={isBusy}
                                        />
                                        <FieldDescription>
                                            6 caractères min., au moins une majuscule et un chiffre.
                                        </FieldDescription>
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            <Controller
                                name="role"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="role">Rôle</FieldLabel>
                                        <select
                                            {...field}
                                            id="role"
                                            className="inline-flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                            aria-invalid={fieldState.invalid}
                                            disabled={isBusy}
                                        >
                                            {roles.map((role) => (
                                                <option key={role} value={role}>
                                                    {role}
                                                </option>
                                            ))}
                                        </select>
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            {apiErrors.length > 0 && (
                                <Field data-invalid>
                                    <FieldError errors={apiErrors.map((message) => ({ message }))} />
                                </Field>
                            )}

                            {successMessage && (
                                <Field>
                                    <p className="text-sm font-medium text-emerald-700">{successMessage}</p>
                                </Field>
                            )}

                            <Field>
                                <Button type="submit" disabled={isBusy} className="w-full">
                                    {isBusy && <Spinner />}
                                    {isBusy ? 'Création...' : 'Créer le compte'}
                                </Button>
                                <FieldDescription className="text-center">
                                    Vous avez déjà un compte ? <Link to="/login">Se connecter</Link>
                                </FieldDescription>
                            </Field>
                        </FieldGroup>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
